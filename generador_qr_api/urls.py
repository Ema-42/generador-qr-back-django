
from django.contrib import admin
from django.urls import include, path

from django.urls import path, include
from qr.views import redirect_qr_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('qr.urls')),

    # Ruta para redirección por ID
    path('<uuid:qr_id>/', redirect_qr_view, name='redirect_qr'),
]
