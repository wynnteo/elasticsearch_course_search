from elasticsearch import Elasticsearch, exceptions
from sentence_transformers import SentenceTransformer

es = Elasticsearch(['http://localhost:9200'])


def index_course(course):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding = model.encode(course.name + " " + course.description).tolist()
    course.embedding = embedding

    doc = {
        'name': course.name,
        'name_suggest': {
            'input': [course.name]
        },
        'description': course.description,
        'category_id': course.category_id,
        'sub_category_id': course.sub_category_id,
        'language': course.language,
        'source': course.source,
        'level': course.level,
        'instructor': course.instructor,
        'is_valid': course.is_valid,
        'modified_at': course.modified_at.isoformat(),
        'embedding': course.embedding 
    }

    try:
        es.index(index='courses_v2', id=course.id, document=doc)
    except exceptions.ElasticsearchException as e:
        print(f"Failed to index course {course.id}: {e.info if hasattr(e, 'info') else str(e)}")
