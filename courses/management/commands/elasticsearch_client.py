from elasticsearch import Elasticsearch, exceptions

es = Elasticsearch(['http://localhost:9200'])

def index_course(course):
    doc = {
        'name': course.name,
        'description': course.description,
        'category_id': course.category_id,
        'sub_category_id': course.sub_category_id,
        'language': course.language,
        'source': course.source,
        'level': course.level,
        'is_valid': course.is_valid,
        'modified_at': course.modified_at.isoformat(),
    }
    try:
        es.index(index='courses', id=course.id, document=doc)
    except exceptions.ElasticsearchException as e:
        print(f"Failed to index course {course.id}: {e.info if hasattr(e, 'info') else str(e)}")
