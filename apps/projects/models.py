from django.db import models


class Projects(models.Model):
    name_project = models.CharField(max_length=200)
    descriptions = models.TextField()


    class Meta:
        db_table = "projectify_projects"
