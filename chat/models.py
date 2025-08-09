from django.db import models

# Create your models here.
from mongoengine import Document, StringField, DateTimeField, DictField, BooleanField

class Message(Document):
    wa_id = StringField(required=True)
    message_id = StringField(required=True, unique=True)
    timestamp = DateTimeField(required=True)
    message = StringField()
    status = StringField(choices=["sent", "delivered", "read"])
    user_info = DictField()  

    meta = {'collection': 'processed_messages'}
