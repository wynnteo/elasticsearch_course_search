from django.core.management.base import BaseCommand
from courses.models import Course
from .elasticsearch_client import es, index_course

class Command(BaseCommand):
    help = 'Index all courses into Elasticsearch'

    def handle(self, *args, **kwargs):
        index_name = 'courses'
        
        if not es.indices.exists(index=index_name):
            self.stdout.write(f"Creating index: courses")
            es.indices.create(index=index_name)

        courses = Course.objects.all()
        for course in courses:
            print(f"Indexing course {course.id} - {course.name}")
            index_course(course)
            self.stdout.write(self.style.SUCCESS(f'Successfully indexed course: {course.name}'))
    
        self.stdout.write(self.style.SUCCESS('Successfully indexed all courses'))
