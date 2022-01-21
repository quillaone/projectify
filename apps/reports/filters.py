from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ReportSerializers
from apps.users.models import User
from apps.projects.models import Projects
from .models import Reports
from rest_framework.pagination import LimitOffsetPagination
from django.db.models.manager import Manager
from datetime import datetime
import django_auto_prefetching
from django_auto_prefetching import AutoPrefetchViewSetMixin
from django.db.models import Case, When

import time
from time import gmtime, strftime


class ReportsFiltersView(APIView, LimitOffsetPagination, AutoPrefetchViewSetMixin):
    serializer_class = ReportSerializers

    def get(self, request):
        try:
            reports = self.filters(request)
            if request.query_params is None:
                reports = reports.all()
            if isinstance(reports, Manager):
                reports = reports.all()
            self.paginate_queryset(reports, request, view=self)
            result = django_auto_prefetching.prefetch(reports, self.serializer_class)
            serializer = ReportSerializers(result, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    def filters(self, request):
        reports = Reports.objects
        reports = reports.select_related()

        if 'user_name' in request.query_params:
            reports = self.filter_user_name(request, reports)
        if 'date_create' in request.query_params:
            reports = self.filter_date_create(request, reports)
        if 'percentage' in request.query_params:
            reports = self.filter_percentage_range(request, reports)
        if 'project_name' in request.query_params:
            reports = self.filter_project_name(request, reports)
        if 'project' in request.query_params or "user":
            reports = self.filter_reports_model(request, reports)
        return reports

    def filter_date_create(self, request, reports):
        try:
            if request.query_params['date_create'].find('&') != -1:
                date_create = request.query_params['date_create'].split('&')
                start_date = datetime.strptime(date_create[0], "%Y-%m-%d")
                end_date = datetime.strptime(date_create[1], "%Y-%m-%d").replace(hour=23, minute=59, second=59)
                reports = reports.filter(date_create__range=(start_date, end_date))
            else:
                date_create = request.query_params['date_create']
                reports = reports.filter(date_create__gte=date_create)
            return reports
        except Exception as error:
            return Response({'error': "Parametro  invalido"}, status=status.HTTP_400_BAD_REQUEST)

    def filter_user_name(self, request, reports):
        user = User.objects
        user = user.filter(name__icontains=request.query_params['user_name']).values('id').distinct()
        reports = reports.select_related('user').filter(user__in=user)
        return reports

    def filter_percentage_range(self, request, reports):
        try:
            if request.query_params['percentage'].find('-') != -1:
                percentage = request.query_params['percentage'].split('-')
                reports = reports.filter(percentage__range=(percentage[0], percentage[1]))
            else:
                percentage = request.query_params['percentage']
                reports = reports.filter(percentage__gte=percentage)
            return reports
        except Exception as error:
            return Response({'error': "Parametro invalido"}, status=status.HTTP_400_BAD_REQUEST)

    def filter_project_name(self, request, reports):
        project = Projects.objects
        project = project.filter(name_project__icontains=request.query_params['project_name']).values('id').distinct()
        reports = reports.filter(project__in=project)
        return reports

    def filter_reports_model(self, request, reports):
        if 'project' in request.query_params:
            reports = reports.filter(project=request.query_params["project"])
        if "user" in request.query_params:
            reports = reports.filter(user=request.query_params["user"])
        return reports
