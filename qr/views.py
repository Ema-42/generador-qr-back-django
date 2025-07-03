from rest_framework import viewsets
from .models import QRCode
from .serializer import QrSerializer

class QRCodeView(viewsets.ModelViewSet):
    """
    ViewSet para manejar los códigos QR.
    Permite listar, crear, actualizar y eliminar códigos QR.
    """
    queryset = QRCode.objects.all()
    serializer_class = QrSerializer
    #permission_classes = [IsAuthenticated]
    
    # Eliminar o comentar este método ya que no tienes campo 'user'
    # def perform_create(self, serializer):
    #     """Guarda el código QR con el usuario autenticado."""
    #     serializer.save(user=self.request.user)