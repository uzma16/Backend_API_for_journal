import random
from rest_framework.viewsets import ModelViewSet
from .serializers import PromptSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Prompt
from permission import IsOwner
from response import CustomJsonRender
from django.utils import timezone
from django.core.cache import cache 

class PromptDetail(ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    renderer_classes = (CustomJsonRender,)
    authentication_classes = [JWTAuthentication]
    permissions = {'default': [IsAuthenticated, IsOwner],
                   'list': [IsAuthenticated],
                   'create': [IsAuthenticated]}

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.permissions['default'])
        return super(PromptDetail, self).get_permissions()

    def get_queryset(self):
        current_time = timezone.now()
        last_update = cache.get('last_prompt_update')
        cached_prompt_ids = cache.get('cached_prompt_ids', None)

        if last_update is None or (current_time - last_update).seconds >= 86400:
            all_prompt_ids = list(Prompt.objects.values_list("id", flat=True))
            sampled_prompt_ids = random.sample(all_prompt_ids, 3)
            cache.set('cached_prompt_ids', sampled_prompt_ids, 86400)  # Cache for one day
            cache.set('last_prompt_update', current_time, 86400)  # Cache for one day
        else:
            sampled_prompt_ids = cached_prompt_ids

        selected_prompts = Prompt.objects.filter(id__in=sampled_prompt_ids)
        return selected_prompts
    
            
    # def get_queryset(self):
    #     # if self.action == 'list':
    #     prompts = list(Prompt.objects.all())
    #     prompts = random.sample(prompts, 3)
    #     return prompts