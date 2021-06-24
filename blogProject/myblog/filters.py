import django_filters
from rest_framework import filters
from django_filters import DateFromToRangeFilter
from django_filters.widgets import RangeWidget
from django.db import models
from .models import Post
from django.contrib.auth.models import User


class PostFilter(django_filters.FilterSet):
    # date_created = DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))

    class Meta:
        model = Post
        fields = {
            'title': ['exact', 'icontains'],
            'content': ['exact', 'icontains']
        }


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    class Meta:
        model = Post
        fields = '__all__'
        # exclude = 'id'

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(author=request.user)


# class CustomPostFilter(django_filters.FilterSet):
#
#     class Meta:
#         model = User
#         fields
#     def filter_queryset(self, request, queryset, view):
#         return self.queryset.filter()
