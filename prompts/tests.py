from django.test import TestCase, RequestFactory
from rest_framework.test import APITestCase
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Prompt
from .serializers import PromptSerializer
from .views import PromptDetail


class PromptDetailTestCase(APITestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()
        self.prompt = mixer.blend(Prompt)
        self.url = reverse('prompt-detail', kwargs={'pk': self.prompt.id})

    def test_get_queryset_action_list(self):
        view = PromptDetail.as_view({'get': 'list'})
        request = self.factory.get(self.url)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Ensure only 3 objects are returned

    def test_get_queryset_action_other_than_list(self):
        view = PromptDetail.as_view({'get': 'retrieve'})
        request = self.factory.get(self.url)
        response = view(request, pk=self.prompt.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, PromptSerializer(self.prompt).data)  # Ensure the serializer is working properly
