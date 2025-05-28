from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page
from django_ratelimit.decorators import ratelimit
from elasticsearch import Elasticsearch
from elasticsearch import exceptions as es_exceptions

from sentence_transformers import SentenceTransformer
import logging
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

# Initialize components once at startup
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Lightweight model for embeddings

def get_elasticsearch_client():
    """Returns configured Elasticsearch client with connection pooling"""
    return Elasticsearch(
        ['http://localhost:9200'],
        max_retries=3,
        retry_on_timeout=True,
        request_timeout=30  # seconds
    )

es = get_elasticsearch_client()

@require_GET
@cache_page(60 * 15)  # Cache for 15 minutes
@ratelimit(key='ip', rate='100/h')  # Prevent abuse
def course_search(request):
    """
    Advanced course search endpoint supporting:
    - Fuzzy search
    - Vector-based semantic search
    - Multi-field search with boosting
    - Smart filtering
    - Highlighting
    - Autocomplete suggestions
    """
    try:
        # Parse and validate parameters
        query = request.GET.get('q', '').strip()
        filters = {
            'level': request.GET.get('level'),
            'category': request.GET.get('category'),
            'language': request.GET.get('lang'),
            'source': request.GET.get('source')
        }
        
        # Generate query embedding for semantic search
        query_embedding = model.encode(query).tolist() if query else []
        print(len(query_embedding))

        # Build complete search request
        search_body = {
            "query": _build_query(query, query_embedding, filters),
            "highlight": _build_highlight_config(),
            "suggest": _build_autocomplete_suggestions(query),
            "size": 20  # Limit results for pagination
        }

        print(search_body)

        # Execute search with timeout
        response = es.search(index='courses_v2', body=search_body, request_timeout=10)
        print(response)
        
        return JsonResponse({
            'results': _process_hits(response['hits']),
            'suggestions': _process_suggestions(response.get('suggest', {})),
            'highlighted': _process_highlights(response.get('highlight', {})),
            'took_ms': response['took']
        })

    except es_exceptions.ApiError as e:
        print(e)
        return JsonResponse({
            "error": "Elasticsearch query failed",
            "details": str(e)
        }, status=500)

    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
        return JsonResponse(
            {'error': 'Internal server error'},
            status=500
        )

def _build_query(query, embedding, filters):
    """Constructs combined fuzzy + vector search query with filters"""
    return {
        "bool": {
            "should": [  # Either match contributes to score
                _build_text_query(query),
                _build_vector_query(embedding)
            ],
            "filter": _build_filters(filters),
            "minimum_should_match": 1  # Require at least one should clause
        }
    }

def _build_text_query(query):
    """Fuzzy search with field boosting and synonyms"""
    return {
        "multi_match": {
            "query": query,
            "fields": [
                "name^3", 
                "description^2",
                "instructor^1.5"
            ],
            "fuzziness": "AUTO",
           # "analyzer": "synonym_analyzer",
            "type": "most_fields"
        }
    }

def _build_vector_query(embedding):
    """Semantic search using precomputed embeddings"""
    if not embedding:
        return {"match_none": {}}
        
    return {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": """
                    (cosineSimilarity(params.query_vector, 'embedding') + 1.0) * _score
                """,
                "params": {"query_vector": embedding}
            }
        }
    }

def _build_vector_query_knn(embedding):
    """Semantic search using k-NN"""
    if not embedding:
        return {"match_none": {}}
        
    return {
        "knn": {
            "field": "embedding",
            "query_vector": embedding,   
            "k": 20,                 # Number of nearest neighbors to return
            "num_candidates": 100,   # Number of candidates to consider for efficiency
            "boost": 0.8             # Weighting factor for ranking
        }
    }

def _build_filters(filters):
    """Construct filter clauses for valid filters"""
    valid_filters = []
    for field, value in filters.items():
        if value:
            valid_filters.append({"term": {field: value}})
    return valid_filters

def _build_highlight_config():
    """Configure highlighted snippets"""
    return {
        "fields": {
            "name": {"number_of_fragments": 0},
            "description": {
                "fragment_size": 150,
                "number_of_fragments": 1
            }
        }
    }

def _build_autocomplete_suggestions(query):
    """Prefix-based suggestions for autocomplete"""
    if not query or len(query) < 3:
        return {}
        
    return {
        "course_suggestions": {
            "prefix": query,
            "completion": {
                "field": "name_suggest",
                "skip_duplicates": True,
                "fuzzy": {"fuzziness": 1}
            }
        }
    }

def _process_hits(hits):
    """Extract and transform search results"""
    return [{
        'id': hit['_id'],
        'score': hit['_score'],
        **hit['_source']
    } for hit in hits.get('hits', [])]

def _process_suggestions(suggestions):
    """Extract autocomplete suggestions"""
    results = []
    for suggestion in suggestions.values():
        if suggestion and len(suggestion) > 0:
            options = suggestion[0].get('options', [])
            results.extend(opt['text'] for opt in options)
    return results

def _process_highlights(highlights):
    """Extract highlighted fragments"""
    return {
        hit_id: {
            field: fragments[0] if fragments else None
            for field, fragments in hit_highlights.items()
        }
        for hit_id, hit_highlights in highlights.items()
    }


def course_search_page(request):
    return render(request, 'course_search.html')