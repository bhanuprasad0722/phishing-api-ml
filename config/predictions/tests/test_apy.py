import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from unittest.mock import patch


@pytest.mark.django_db
class TestPredictionAPI:

    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    @pytest.fixture
    def auth_client(self, api_client, user):
        api_client.force_authenticate(user=user)
        return api_client

    def test_unauthorized_access(self, api_client):
        url = reverse("predict")
        response = api_client.post(url, {"url": "http://example.com"})
        assert response.status_code == 401

    def test_missing_url(self, auth_client):
        url = reverse("predict")
        response = auth_client.post(url, {})
        assert response.status_code == 400

    @patch("predictions.ml_model.predict")
    def test_valid_prediction(self, mock_predict, auth_client):
        mock_predict.return_value = ("phishing", 0.91)

        url = reverse("predict")
        response = auth_client.post(
            url,
            {"url": "http://fake-login.com"},
            format="json"
        )

        assert response.status_code == 200
        assert response.data["prediction"] == "phishing"
        assert response.data["confidence"] == 0.91

