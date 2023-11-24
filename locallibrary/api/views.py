from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import BookSerializer
from catalog.models import Book


class BookList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        books = Book.objects.all()
        data = BookSerializer(books, many=True).data
        return Response(data)
