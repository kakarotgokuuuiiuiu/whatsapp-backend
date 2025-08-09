from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    wa_id = serializers.CharField()
    message_id = serializers.CharField()
    timestamp = serializers.DateTimeField()
    message = serializers.CharField()
    status = serializers.CharField()
    user_info = serializers.DictField()
