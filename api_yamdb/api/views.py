from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Categories, Genres, Titles
from .mixins import CreateListRetrieveDestroyViewSet
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitleCreateSerializer,
                          TitleReadSerializer)


class CategoriesViewSet(CreateListRetrieveDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(CreateListRetrieveDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return TitleCreateSerializer
        return TitleReadSerializer
