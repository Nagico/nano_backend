from rest_framework import serializers

from .models import Staff


class StaffInfoSerializer(serializers.ModelSerializer):
    """
    Staff 简要序列化器
    """
    class Meta:
        model = Staff
        fields = ['id', 'name']


class StaffDetailSerializer(StaffInfoSerializer):
    """
    Staff 详细序列化器
    """
    class Meta:
        model = Staff
        fields = '__all__'
