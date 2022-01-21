from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Projects
from .serializers import ProjectsSerializers
from rest_framework.pagination import LimitOffsetPagination
import django_auto_prefetching
from django_auto_prefetching import AutoPrefetchViewSetMixin


class ProjectsListView(APIView, LimitOffsetPagination, AutoPrefetchViewSetMixin):
    serializer_class = ProjectsSerializers
    # GET ALL
    def get(self, request):
        try:
            projects = Projects.objects.all()
            projects = projects.select_related()
            self.paginate_queryset(projects, request, view=self)
            results = django_auto_prefetching.prefetch(projects, self.serializer_class)
            serializer = ProjectsSerializers(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            datos = {'message': str(error)}
            return Response(datos, status=status.HTTP_204_NO_CONTENT)

    # CREATE
    def post(self, request):
        try:
            serializers = ProjectsSerializers(data=request.data)
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


class ProjectDetailView(APIView, LimitOffsetPagination, AutoPrefetchViewSetMixin):
    serializer_class = ProjectsSerializers

    # GET ID
    def get(self, request, pk=None):
        try:
            project = Projects.objects.filter(id=pk)
            project = project.select_related()
            self.paginate_queryset(project, request, view=self)
            results = django_auto_prefetching.prefetch(project, self.serializer_class)
            serializer = ProjectsSerializers(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_204_NO_CONTENT)

    # UPDATE
    def put(self, request, pk=None):
        try:
            project = Projects.objects.get(id=pk)
            serializers = ProjectsSerializers(project, data=request.data, partial=True)
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
            project = Projects.objects.get(id=pk).delete()
            datos = {'message': "delete success"}
            return Response(datos, status=status.HTTP_200_OK)
        except Exception as error:
            datos = {'message':
                         ["no found!!!"]}
            return Response(datos, status=status.HTTP_204_NO_CONTENT)
