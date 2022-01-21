from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User as UserModel
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime as dt


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = UserModel.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')

        utiltime = {
            'id': user.id,
            'exp': dt.datetime.utcnow() + dt.timedelta(minutes=60),
            'iat': dt.datetime.utcnow()
        }
        token = jwt.encode(utiltime, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}
        return response


class User(APIView):
    def get(self, request):
        token = request.COOKIES.get ('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!!!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!!!')

        user = UserModel.objects.filter(id = payload ['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogOut(APIView):
    def post (self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':
                "success"
        }
        return  response