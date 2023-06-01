from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model, authenticate

userModel = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        # pass
        model = userModel
        fields = [

            'uid',
            'username',
            'email',
            'profileImage',
            'address',
            'phone',
            'user_category',
            'registered_on',
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # pass
        model = userModel
        fields = [

            'uid',
            'username',
            'email',
            'password',
            'profileImage',
            'address',
            'phone',
            'user_category',
            'registered_on',
        ]

    def create(self, validated_data):
        userObject = userModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )
        userObject.save()
        return userObject


class UserLogin(serializers.Serializer):
    email = serializers.EmailField()

    # password = serializers.CharField()

    class Meta:
        # pass
        model = userModel
        fields = [

            'uid',
            'username',
            'email',
            'address',
            'phone']

    def checkLogin(self, clean_data):
        user_obj = authenticate(
            username=clean_data['email'], password=clean_data['password'])
        if not user_obj:
            raise ValueError('user not found')
        return user_obj


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        # pass
        model = Product
        fields = [

            'user_id',
            'product_id',
            'product_name',
            'description',
            'product_price',
            'product_image',
            'product_category',
            'date_created',
            'condition',
        ]


# class UserStoreSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = UserStore
#         fields = [


#             'user_id',
#             'store_name',
#             'created_on',
#         ]
