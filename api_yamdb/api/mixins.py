from rest_framework import mixins, viewsets


class CreateListRetrieveDestroyViewSet(mixins.CreateModelMixin,
                                       mixins.ListModelMixin,
                                       mixins.RetrieveModelMixin,
                                       mixins.DestroyModelMixin,
                                       viewsets.GenericViewSet):

    pass
