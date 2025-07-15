from rest_framework import viewsets, status
from .models import QRCode,QRScan
from .serializer import QrSerializer, QRScanSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
import qrcode
from io import BytesIO
from django.http import HttpResponse
import base64
from rest_framework.permissions import AllowAny
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import *
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    RoundedModuleDrawer,
    CircleModuleDrawer,
    SquareModuleDrawer,
    GappedSquareModuleDrawer,
    VerticalBarsDrawer,
    HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask,
    RadialGradiantColorMask,
    SquareGradiantColorMask,
    HorizontalGradiantColorMask,
    VerticalGradiantColorMask
)
from PIL import Image
import base64
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import *
from qrcode.image.styles.colormasks import *

from django.http import JsonResponse, Http404
from django.views.decorators.http import require_GET
from django.utils.timezone import now
import os
from django.shortcuts import get_object_or_404
@require_GET
def redirect_qr_view(request, qr_id):
    qr = get_object_or_404(QRCode, id=qr_id)

    try:
        qr.views_count += 1
        qr.last_viewed_at = now()
        qr.save(update_fields=['views_count', 'last_viewed_at'])
        ip = get_client_ip(request)
        QRScan.objects.create(
            qr=qr,
            ip=ip if ip else None
        )
    except Exception as e:
        print(f"Error actualizando QR: {e}")
        raise Http404("Error al registrar la vista del QR")

    return JsonResponse({'redirect_to': qr.content})

def get_client_ip(request):
    """Función util para extraer la IP"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost')


class QRCodeView(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QrSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_eliminated = True
        instance.save(update_fields=["is_eliminated"])
        return Response({"message": "QR eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return QRCode.objects.filter(is_eliminated=False)

    @action(detail=True, methods=['get'], url_path='views', url_name='qr-views')
    def get_views(self, request, pk=None):
        try:
            qr_instance = QRCode.objects.get(pk=pk)
        except QRCode.DoesNotExist:
            return Response({'detail': 'QR no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        scans = QRScan.objects.filter(qr=qr_instance).order_by('-time')
        serializer = QRScanSerializer(scans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='image', permission_classes=[AllowAny])
    def get_qr_image_base64(self, request, pk=None):
        from django.shortcuts import get_object_or_404
        qr = get_object_or_404(QRCode, id=pk)

        if qr.qr_base64:
            return Response({"qr_image_base64": qr.qr_base64}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Este QR no tiene una imagen almacenada."}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=['post'], url_path='generar', permission_classes=[AllowAny])
    def generar_qr(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content_seguimiento = None

        content = request.data.get("content")
        #content = qr_instance.content
        style = request.data.get("style", "square").lower()
        color_hex = request.data.get("color", "#000000")
        gradient = request.data.get("gradient", "").lower()
        gradient_color_hex = request.data.get("gradient_color", "#000000")

        if request.data.get("register_as_official", False):
            qr_instance = serializer.save()
            content_seguimiento = f"{frontend_url}/{qr_instance.id}"
        else:
            content_seguimiento = content

        # Color de fondo (opcional)
        background_hex = request.data.get("background_color", "#ffffff")
        if background_hex.lower() == "transparent":
            background_color = (255, 255, 255, 0)  # blanco transparente en RGBA
        else:
            background_color = hex_to_rgb(background_hex)

        border = int(request.data.get("border", 4))
        border = max(0, min(border, 10))

        color = hex_to_rgb(color_hex)
        gradient_color = hex_to_rgb(gradient_color_hex)

        style_map = {
            "square": SquareModuleDrawer(),
            "circle": CircleModuleDrawer(),
            "rounded": RoundedModuleDrawer(),
            "gapped": GappedSquareModuleDrawer(),
            "vertical": VerticalBarsDrawer(),
            "horizontal": HorizontalBarsDrawer(),
        }
        module_drawer = style_map.get(style, SquareModuleDrawer())

        # Color mask
        if gradient == "radial":
            color_mask = RadialGradiantColorMask(
                back_color=background_color or (255, 255, 255),
                center_color=color,
                edge_color=gradient_color
            )
        elif gradient == "square":
            color_mask = SquareGradiantColorMask(
                back_color=background_color or (255, 255, 255),
                center_color=color,
                edge_color=gradient_color
            )
        elif gradient == "horizontal":
            color_mask = HorizontalGradiantColorMask(
                back_color=background_color or (255, 255, 255),
                left_color=color,
                right_color=gradient_color
            )
        elif gradient == "vertical":
            color_mask = VerticalGradiantColorMask(
                back_color=background_color or (255, 255, 255),
                top_color=color,
                bottom_color=gradient_color
            )
        else:
            color_mask = SolidFillColorMask(
                front_color=color,
                back_color=background_color
            )

        # Crear objeto QR
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            border=border,
        )
        qr.add_data(content_seguimiento)
        qr.make(fit=True)

        # Imagen embebida (opcional)
        embedded_image_base64 = request.data.get("embedded_image", None)
        embedded_image = None

        if embedded_image_base64:
            try:
                image_data = base64.b64decode(embedded_image_base64)
                embedded_image = Image.open(BytesIO(image_data))
                if embedded_image.mode != 'RGBA':
                    embedded_image = embedded_image.convert('RGBA')


            except Exception as e:
                embedded_image = None
                print(f"Error procesando imagen embebida: {e}")

        # Generar imagen QR
        # Generar imagen QR sin imagen embebida primero
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=module_drawer,
            color_mask=color_mask,
        )

        # Si hay imagen embebida, superponerla manualmente
        if embedded_image:
            # Convertir a RGBA si no lo está
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # Calcular el tamaño deseado para la imagen embebida
            qr_width, qr_height = img.size
            embed_ratio = float(request.data.get("embed_ratio", 0.30))  # 8% del QR
            embed_size = int(min(qr_width, qr_height) * embed_ratio)

            # Redimensionar la imagen embebida
            embedded_resized = embedded_image.resize((embed_size, embed_size), Image.LANCZOS)

            # Calcular posición central
            x = (qr_width - embed_size) // 2
            y = (qr_height - embed_size) // 2

            # Superponer la imagen
            img.paste(embedded_resized, (x, y), embedded_resized)

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        image_png = buffer.getvalue()
        buffer.close()

        image_base64 = base64.b64encode(image_png).decode('utf-8')
        #guarrdar image_base64  en el campo qr_base64 del modelo
        if request.data.get("register_as_official", False):
            qr_instance.qr_base64 = image_base64
            qr_instance.save(update_fields=['qr_base64'])

        return Response({
            "content": content,
            "register_as_official": request.data.get("register_as_official", False),
            "qr_image_base64": image_base64

        }, status=status.HTTP_201_CREATED)