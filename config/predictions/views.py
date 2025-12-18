from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serialization import PredictionSerializer
from .ml_model import predict

class PredictAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = PredictionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        url = serializer.validated_data["url"]

        label, confidence = predict(url)

        return Response({
            "url": url,
            "prediction": label,
            "confidence": confidence
        })
