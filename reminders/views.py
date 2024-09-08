from rest_framework.viewsets import ModelViewSet
from .serializers import ReminderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from pagination import StandardResultsSetPagination
from .models import Reminder
from permission import IsOwner
from response import CustomJsonRender

# Create your views here.
class ReminderDetail(ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    pagination_class = StandardResultsSetPagination
    renderer_classes = (CustomJsonRender,)
    authentication_classes = [JWTAuthentication]
    permissions = {'default': [IsAuthenticated, IsOwner],
                   'list': [IsAuthenticated],
                   'create': [IsAuthenticated]}

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super(ReminderDetail, self).get_permissions()

    def get_queryset(self):
        if self.action == 'list':
            return super().get_queryset().filter(user=self.request.user).order_by('-time')
        return super().get_queryset()
