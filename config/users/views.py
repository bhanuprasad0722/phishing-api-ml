from django.shortcuts import render
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions

class Register(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        serializer = RegisterSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response (
                {"message" : "User Registered Sucessfully"},
                status = status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

