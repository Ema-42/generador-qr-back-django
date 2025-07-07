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

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
class QRCodeView(viewsets.ModelViewSet):
    queryset = QRCode.objects.all()
    serializer_class = QrSerializer

    @action(detail=False, methods=['post'], url_path='generar', permission_classes=[AllowAny])
    def generar_qr(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qr_instance = serializer.save()

        content = qr_instance.content
        style = request.data.get("style", "square").lower()
        color_hex = request.data.get("color", "#000000")
        gradient = request.data.get("gradient", "").lower()
        gradient_color_hex = request.data.get("gradient_color", "#000000")

        # Color de fondo (opcional)
        background_hex = request.data.get("background_color", "#ffffff")
        if background_hex.lower() == "transparent":
            background_color = (255, 255, 255, 0)  # blanco transparente en RGBA
        else:
            background_color = hex_to_rgb(background_hex)

        # Limitar valores de tamaño
        box_size = int(request.data.get("box_size", 10))
        box_size = max(1, min(box_size, 20))

        border = int(request.data.get("border", 4))
        border = max(0, min(border, 10))

        # Convertir colores a RGB
        color = hex_to_rgb(color_hex)
        gradient_color = hex_to_rgb(gradient_color_hex)

        # Módulo de dibujo
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
        gradient_map = {
            "radial": RadialGradiantColorMask,
            "square": SquareGradiantColorMask,
            "horizontal": HorizontalGradiantColorMask,
            "vertical": VerticalGradiantColorMask,
        }

        if gradient in gradient_map:
            color_mask = gradient_map[gradient](
                back_color=background_color or (255, 255, 255),
                center_color=color,
                edge_color=gradient_color
            )
        else:
            color_mask = SolidFillColorMask(
                front_color=color,
                back_color=background_color
            )

        # Crear objeto QR
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=box_size,
            border=border,
        )
        qr.add_data(content)
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
            embed_ratio = float(request.data.get("embed_ratio", 0.15))  # 8% del QR
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

        return Response({
            "id": qr_instance.id,
            "content": content,
            "style": style,
            "color": color,
            "gradient": gradient,
            "gradient_color": gradient_color,
            "background_color": background_hex,
            "box_size": box_size,
            "border": border,
            "has_embedded_image": embedded_image is not None,
            "qr_image_base64": image_base64
        }, status=status.HTTP_201_CREATED)


