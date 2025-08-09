from rest_framework.decorators import api_view
from rest_framework.response import Response
from chat.models import Message
from datetime import datetime

@api_view(['GET'])
def unique_users(request):
    users = Message.objects().distinct('wa_id')
    user_info = []
    for wa_id in users:
        latest = Message.objects(wa_id=wa_id).order_by('-timestamp').first()
        if latest:
            user_info.append({
                "wa_id": wa_id,
                "name": latest.user_info.get("name"),
                "number": latest.user_info.get("number"),
            })
    return Response(user_info)

@api_view(['GET'])
def get_messages(request):
    """Return all messages"""
    messages = Message.objects().order_by('timestamp')
    data = []
    for msg in messages:
        data.append({
            "wa_id": msg.wa_id,
            "message_id": msg.message_id,
            "timestamp": msg.timestamp,
            "message": msg.message,
            "status": msg.status,
            "user_info": msg.user_info
        })
    return Response(data)

@api_view(['GET'])
def get_messages_by_user(request, wa_id):
    """Return messages for a specific user (chat thread)"""
    messages = Message.objects(wa_id=wa_id).order_by('timestamp')
    data = []
    for msg in messages:
        data.append({
            "wa_id": msg.wa_id,
            "message_id": msg.message_id,
            "timestamp": msg.timestamp,
            "message": msg.message,
            "status": msg.status,
            "user_info": msg.user_info
        })
    return Response(data)

@api_view(['POST'])
def send_message(request):
    """Save a new message to the database (demo only — no WhatsApp API call)"""
    data = request.data
    wa_id = data.get("wa_id")
    name = data.get("name")
    message_text = data.get("message")

    if not wa_id or not message_text:
        return Response({"error": "wa_id and message are required"}, status=400)

    
    msg = Message(
        wa_id=wa_id,
        message_id=f"local_{datetime.utcnow().timestamp()}",  
        timestamp=datetime.utcnow(),
        message=message_text,
        status="sent",
        user_info={"name": name, "number": wa_id}
    )
    msg.save()

    return Response({
        "success": True,
        "message": {
            "wa_id": msg.wa_id,
            "message_id": msg.message_id,
            "timestamp": msg.timestamp,
            "message": msg.message,
            "status": msg.status,
            "user_info": msg.user_info
        }
    })

@api_view(['POST'])
def update_message_status(request):
    message_id = request.data.get("message_id")
    status = request.data.get("status")
    if not message_id or status not in ["sent", "delivered", "read"]:
        return Response({"error": "Invalid data"}, status=400)

    msg = Message.objects(message_id=message_id).first()
    if not msg:
        return Response({"error": "Message not found"}, status=404)

    msg.status = status
    msg.save()
    return Response({"success": True, "message_id": message_id, "status": status})
