from rest_framework import serializers
from .models import Reports
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
import time
from time import gmtime, strftime
from apps.projects.serializers import ProjectsSerializers


class ReportSerializers(serializers.ModelSerializer):

    class Meta():
        model = Reports
        fields = '__all__'

