import datetime
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from catalog.models import Book, BookInstance


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = '__all__'


class RenewBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ['due_back']

    def validate_due_back(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError(_('Invalid date - renewal in the past'))

        if value > datetime.date.today() + datetime.timedelta(weeks=4):
            raise serializers.ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return value
