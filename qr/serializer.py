from rest_framework import serializers
from .models import QRCode,QRScan

class QrSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = ['id', 'content', 'nombre_qr', 'created_at', 'views_count','last_viewed_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        return QRCode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

class QRScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRScan
        fields = ['id', 'qr', 'ip', 'time']