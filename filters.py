'''
Created on Nov 8, 2014

@author: nanaya
'''
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils import six

from rest_framework.filters import BaseFilterBackend
from rest_framework.settings import api_settings
from functools import reduce
import operator


class SearchFilter(BaseFilterBackend):
    """
    Filtering against query parameters.

    Specify the fields by which you want to filter the queryset 
    in search_fields with the form of (field_name, url_param).
    """
    def get_search_terms(self, request, search_fields):
        return [request.QUERY_PARAMS.get(field, None)
                for field in search_fields]

    def construct_search(self, field_name):
        if field_name.startswith('^'):
            return "%s__istartswith" % field_name[1:]
        elif field_name.startswith('='):
            return "%s__exact" % field_name[1:]
        elif field_name.startswith('@'):
            return "%s__search" % field_name[1:]
        elif field_name.startswith('>'):
            return "%s__gt" % field_name[1:]
        elif field_name.startswith('<'):
            return "%s__lt" % field_name[1:]
        else:
            return "%s__icontains" % field_name

    def filter_queryset(self, request, queryset, view):
        search_params = getattr(view, 'search_fields', None)

        if not search_params:
            return queryset

        url_params = []
        search_fields = []
        for search_param in search_params:
            if isinstance(search_param, tuple) and len(search_param) > 1:
                search_fields.append(search_param[0])
                url_params.append(search_param[1])
            else:
                search_fields.append(search_param)
                url_params.append(search_param)

        orm_lookups = [self.construct_search(str(search_field))
                       for search_field in search_fields]
        search_terms = self.get_search_terms(request, url_params)

        Q_expressions = {
            orm_lookup: search_term
            for orm_lookup, search_term in zip(orm_lookups, search_terms)
            if search_term is not None
        }
        if Q_expressions:
            and_queries = [models.Q(**{k: v})
                           for k, v in Q_expressions.items()]
            queryset = queryset.filter(reduce(operator.and_, and_queries))
        return queryset


class OrderingFilter(BaseFilterBackend):
    # The URL query parameter used for the ordering.
    ordering_param = api_settings.ORDERING_PARAM
    ordering_fields = None

    def get_ordering(self, request):
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.
        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        params = request.QUERY_PARAMS.get(self.ordering_param)
        if params:
            return [param.strip() for param in params.split(',')]

    def get_default_ordering(self, view):
        ordering = getattr(view, 'ordering', None)
        if isinstance(ordering, six.string_types):
            return (ordering,)
        return ordering

    def remove_invalid_fields(self, queryset, ordering, view):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)

        if valid_fields is None:
            # Default to allowing filtering on serializer fields
            serializer_class = getattr(view, 'serializer_class')
            if serializer_class is None:
                msg = ("Cannot use %s on a view which does not have either a "
                       "'serializer_class' or 'ordering_fields' attribute.")
                raise ImproperlyConfigured(msg % self.__class__.__name__)
            valid_fields = [
                field.source or field_name
                for field_name, field in serializer_class().fields.items()
                if not getattr(field, 'write_only', False)
            ]
        elif valid_fields == '__all__':
            # View explictly allows filtering on any model field
            valid_fields = [field.name for field in queryset.model._meta.fields]
            valid_fields += queryset.query.aggregates.keys()

        return [term for term in ordering if term.lstrip('-') in valid_fields]

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request)

        if ordering:
            # Skip any incorrect parameters
            ordering = self.remove_invalid_fields(queryset, ordering, view)

        if not ordering:
            # Use 'ordering' attribute by default
            ordering = self.get_default_ordering(view)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset
