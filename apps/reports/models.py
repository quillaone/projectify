from django.db import models
from apps.users.models import User
from apps.projects.models import Projects
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
import time
from time import gmtime, strftime
from datetime import datetime


class Reports(models.Model):
    project = models.ForeignKey(Projects, to_field='id', related_name='projects',  on_delete=models.CASCADE)
    user = models.ForeignKey(User, to_field='id', related_name='users', on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=False, auto_now=False)
    percentage = models.FloatField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    week_number = models.IntegerField(validators=[MaxValueValidator(70), MinValueValidator(0)])

    class Meta:
        db_table = "projectify_reports"
