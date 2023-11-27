from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from api.permissions import CanMarkReturned
from api.serializers import BookSerializer, RenewBookSerializer, BookInstanceSerializer
from catalog.models import Book, BookInstance


class BookList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        books = Book.objects.all()
        data = BookSerializer(books, many=True).data
        return Response(data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        data = BookSerializer(book).data

        return Response(data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        instance = BookInstance.objects.filter(book=book)

        if instance:
            return Response({"message": "Book has instance"}, status=status.HTTP_400_BAD_REQUEST)

        book.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AllBorrowedList(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        book_instances = BookInstance.objects.all()
        data = BookInstanceSerializer(book_instances, many=True).data
        return Response(data)


class RenewBook(APIView):
    permission_classes = (IsAuthenticated, CanMarkReturned)

    def get_object(self, pk):
        try:
            return BookInstance.objects.get(pk=pk)
        except BookInstance.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        book_instance = self.get_object(pk)
        serializer = RenewBookSerializer(book_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
