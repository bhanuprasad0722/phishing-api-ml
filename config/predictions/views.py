from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serialization import PredictionSerializer
from .ml_model import predict

class PredictAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PredictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]

        # Auto-add http/https if missing
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        try:
            label, confidence = predict(url)
            return Response({
                "url": url,
                "prediction": label,
                "confidence": confidence
            })
        except Exception as e:
            # Catch ML or feature extraction errors
            return Response({
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
