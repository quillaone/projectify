from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.pagination import LimitOffsetPagination
import django_auto_prefetching
from django_auto_prefetching import AutoPrefetchViewSetMixin


# Create your views here.
class UserListView(APIView, LimitOffsetPagination, AutoPrefetchViewSetMixin):
    serializer_class = UserSerializer

    # GET ALL
    def get(self, request):
        try:
            users = User.objects.all()
            users = users.select_related()
            self.paginate_queryset(users, request, view=self)
            results = django_auto_prefetching.prefetch(users, self.serializer_class)
            serializer = UserSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            datos = {'message': str(error)}
            return Response(datos, status=status.HTTP_204_NO_CONTENT)

    # CREATE
    def post(self, request):
        try:
            serializers = UserSerializer(data=request.data)
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


class UserDetailView(APIView, LimitOffsetPagination, AutoPrefetchViewSetMixin):
    serializer_class = UserSerializer

    # GET filter ID
    def get(self, request, pk=None):
        try:
            user = User.objects.filter(id=pk)
            user = user.select_related()
            self.paginate_queryset(user, request, view=self)
            results = django_auto_prefetching.prefetch(user, self.serializer_class)
            serializer = UserSerializer(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            return Response({'message': str(error)}, status=status.HTTP_204_NO_CONTENT)

    # UPDATE
    def put(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            serializers = UserSerializer(user, data=request.data, partial=True)
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
            user = User.objects.get(id=pk).delete()
            datos = {'message': "delete success"}
            return Response(datos, status=status.HTTP_200_OK)
        except Exception as error:
            datos = {'message':
                         ["no found!!!"]}
            return Response(datos, status=status.HTTP_204_NO_CONTENT)
