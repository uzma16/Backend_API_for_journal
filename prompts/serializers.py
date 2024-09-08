from .models import Prompt
from rest_framework import serializers


class PromptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prompt
        fields = ['id', 'title', 'description', 'category', 'audio', 'image', 'color']
