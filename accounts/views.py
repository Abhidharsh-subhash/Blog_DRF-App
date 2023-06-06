from django.shortcuts import render
#it should be in the second otherwise it will not work 
from django.contrib.auth import authenticate
from .serializers import SignUpSerializer
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
# Create your views here.

class SignUpView(GenericAPIView):
    serializer_class=SignUpSerializer
    def post(self,request:Request):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response={
                'message':'User created successfully',
                'data':serializer.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []
    def post(self,request:Request):
        email=request.data.get('email')
        password=request.data.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
            response={
                'message':'Login successfull',
                'token':user.token.key
            }
            return Response(data=response,status=status.HTTP_200_OK)
        else:
            return Response(data={'message':'Invalid email or password'},status=status.HTTP_401_UNAUTHORIZED)
    def get(self,request:Request):
        print('get')
        content={
            "user":str(request.user),
            "auth":str(request.auth)
        }
        return Response(data=content,status=status.HTTP_200_OK)
