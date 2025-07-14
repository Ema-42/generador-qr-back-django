import uuid
from django.db import models
from django.contrib.auth.models import User

class QRCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    nombre_qr = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='qrcodes_creados'
    )
    views_count = models.PositiveIntegerField(default=0)
    last_viewed_at = models.DateTimeField(null=True, blank=True)
    qr_base64 = models.TextField(blank=True, null=True)
    is_eliminated = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.nombre_qr or self.content[:30]

class QRScan(models.Model):
    id = models.AutoField(primary_key=True)
    qr = models.ForeignKey(
        QRCode,
        on_delete=models.CASCADE,
        related_name='scans'
    )
    ip = models.CharField(max_length=45, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scan de {self.qr_id} en {self.time}"
