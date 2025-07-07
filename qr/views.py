from rest_framework import viewsets, status
from .models import QRCode
from .serializer import QrSerializer

from rest_framework.response import Response
from rest_framework.decorators import action
import qrcode
from io import BytesIO
from django.http import HttpResponse
import base64
from rest_framework.permissions import AllowAny
class QRCodeView(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QrSerializer

    @action(detail=False, methods=['post'], url_path='generar', permission_classes=[AllowAny])
    def generar_qr(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 1. Guardar usando el serializer
        qr_instance = serializer.save()

        # 2. Generar imagen QR
        qr = qrcode.make(qr_instance.content)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        image_png = buffer.getvalue()
        buffer.close()

        image_base64 = base64.b64encode(image_png).decode('utf-8')

        return Response({
            "id": qr_instance.id,
            "content": qr_instance.content,
            "qr_image_base64": image_base64
        }, status=status.HTTP_201_CREATED)
