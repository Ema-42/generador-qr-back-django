import uuid
from django.db import models
from django.contrib.auth.models import User

class QRCode(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
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

    def __str__(self):
        return self.nombre_qr or self.content[:30]
