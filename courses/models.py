from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category_id = models.IntegerField()
    sub_category_id = models.IntegerField()
    language = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    instructor = models.CharField(max_length=150)
    level = models.CharField(max_length=50, blank=True, null=True)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.name