from rest_framework.viewsets import ModelViewSet
from .serializers import JournalSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from pagination import StandardResultsSetPagination
from .filters import JournalFilter
from .models import Journal
from permission import IsOwner
from response import CustomJsonRender


class JournalDetail(ModelViewSet):
    """
    Crud APIs for Journals
    """

    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    filterset_class = JournalFilter
    filter_backends = (DjangoFilterBackend, SearchFilter, )
    search_fields = ['description', 'transcript', 'created_at__date']
    renderer_classes = (CustomJsonRender,)
    pagination_class = StandardResultsSetPagination
    authentication_classes = [JWTAuthentication]
    permissions = {'default': [IsAuthenticated, IsOwner],
                   'list': [IsAuthenticated],
                   'create': [IsAuthenticated]}

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super(JournalDetail, self).get_permissions()

    def get_queryset(self):
        if self.action == 'list':
            return super().get_queryset().filter(user=self.request.user).order_by('-created_at')
        return super().get_queryset()
