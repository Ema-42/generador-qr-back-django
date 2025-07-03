from rest_framework import serializers
from .models import QRCode

class QrSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        return QRCode.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance