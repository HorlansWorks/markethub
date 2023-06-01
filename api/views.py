from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import *
from .serializers import *
from .permissions import *


# Create your views here.


class Login(APIView):
    permission_classes = (permissions.AllowAny,)
    # authentication_classes = (SessionAuthentication,)

    def post(self, request):

        data = request.data
        serializer = UserLogin(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.checkLogin(data)
            login(request, user)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccount(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):

        user = request.user
        query = User.objects.get(email=user.email)
        serializer = self.serializer_class(instance=query)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LogOut(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_product_by_user_id(request, user_id):

    queryset = Product.objects.filter(user_id=user_id)
    serialized = ProductSerializer(queryset, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def products_by_category(request, product_category):

    queryset = Product.objects.filter(product_category=product_category)
    serialized = ProductSerializer(queryset, many=True)
    return Response(serialized.data)


@api_view(['GET'])
def home_page(request):

    return Response({" path('products/'": "Products",
                     "path('users/create'": "CreateUser",
                     "path('users/profile'": "User Profile get",
                     "path('auth/jwt/create'": "login with jwt user)",
                     "path('users/all'": "List all Users",
                     "path('users/<uuid:uid>'": "UserById =>  RetrieveUpdateDestroy",
                     "path('products/<uuid:product_id>/'": "ProductById  => RetrieveUpdateDestroy",
                     "path('products/users/<uuid:user_id>/'": "get products by user id"})


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ListUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
#


class UserById(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class Products(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, ProductPermission]


class ProductById(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'product_id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductByUserId(generics.ListAPIView):
    # queryset = Product.objects.filter()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'user_id'


# class ProductByCategory(generics.ListAPIView):
#     queryset = Product.objects.filter()
#     serializer_class = ProductSerializer
#     lookup_field = 'product_category'
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
