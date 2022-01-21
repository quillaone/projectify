from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ReportSerializers
from .models import Reports
from rest_framework.pagination import LimitOffsetPagination
import django_auto_prefetching
from django_auto_prefetching import AutoPrefetchViewSetMixin
from datetime import datetime
import time
from time import gmtime, strftime


class ReportsListView(APIView, LimitOffsetPagination, AutoPrefetchViewSetMixin):
    serializer_class = ReportSerializers

    # GET ALL
    def get(self, request):
        try:
            reports = Reports.objects.all()
            reports = reports.select_related()
            self.paginate_queryset(reports, request, view=self)
            results = django_auto_prefetching.prefetch(reports, self.serializer_class)
            serializer = ReportSerializers(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            datos = {'message': str(error)}
            return Response(datos, status=status.HTTP_204_NO_CONTENT)

    # CREATE
    def post(self, request):
        try:
            date_create = datetime.strptime(request.data["date_create"], "%Y-%m-%d")
            request.data["date_create"] = date_create
            request.data["week_number"] = date_create.isocalendar()[1]
            reportes = Reports.objects.filter(week_number=request.data["week_number"], user_id=request.data["user"],
                                              project_id=request.data["project"])
            if len(reportes) > 0:
                datos = {'message': "Error: there is a report in the same week",
                         'result': {}}
                return Response(datos, status=status.HTTP_400_BAD_REQUEST)

            serializers = ReportSerializers(data=request.data)
            if serializers.is_valid():
                serializers.save()
                datos = {'message': "success created",
                         'result': serializers.data}
                return Response(datos, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            datos = {'message':
                         str(error)}
            return Response(datos, status=status.HTTP_400_BAD_REQUEST)


class ReportDetailView(APIView, LimitOffsetPagination, AutoPrefetchViewSetMixin):
    serializer_class = ReportSerializers

    # GET ID
    def get(self, request, pk=None):
        try:
            report = Reports.objects.filter(id=pk)
            report = report.select_related()
            self.paginate_queryset(report, request, view=self)
            results = django_auto_prefetching.prefetch(report, self.serializer_class)
            serializer = ReportSerializers(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_204_NO_CONTENT)

    # UPDATE
    def put(self, request, pk=None):
        try:
            report = Reports.objects.get(id=pk)
            serializers = ReportSerializers(report, data=request.data, partial=True)
            if serializers.is_valid():
                serializers.save()
                datos = {'message': "update success",
                         'result': serializers.data}
                return Response(datos, status=status.HTTP_200_OK)
            else:
                return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            datos = {'error': str(error)}
            return Response(datos, status=status.HTTP_204_NO_CONTENT)

    # DELETE
    def delete(self, request, pk=None):
        try:
            report = Reports.objects.get(id=pk).delete()
            datos = {'message': "delete success"}
            return Response(datos, status=status.HTTP_200_OK)
        except Exception as error:
            datos = {'message':
                         ["no found!!!"]}
            return Response(datos, status=status.HTTP_204_NO_CONTENT)

#
