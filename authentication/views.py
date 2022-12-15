from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignUpSerializer


class SignUpView(APIView):

    serializer_class = SignUpSerializer

    def get(self, request):
        return Response(
                data={"Welcome, you have to subscribe before accessing API.",
                      "Once it's done, please contact an admin to set your permissions"},
                status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
