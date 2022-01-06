from rest_framework import serializers
from .models import Book
class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    author = serializers.CharField(max_length=100)
    publisher = serializers.CharField(max_length=100)

    def create(self, validate_data):
        return Book.objects.create(**validate_data)
