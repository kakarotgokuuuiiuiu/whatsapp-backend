import os
import json
from datetime import datetime

from django.core.management.base import BaseCommand
from chat.models import Message  # MongoEngine model

class Command(BaseCommand):
    help = 'Process WhatsApp webhook payloads and insert into MongoDB'

    def handle(self, *args, **kwargs):
        folder_path = './payloads'

        for file_name in os.listdir(folder_path):
            if not file_name.endswith('.json'):
                continue

            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:  # ✅ FIXED: UTF-8 encoding
                    payload = json.load(f)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Failed to load {file_name}: {str(e)}"))
                continue

            # ✅ Extract entries from metadata
            meta = payload.get("metaData", {})
            entry_list = meta.get("entry", [])
            if not entry_list:
                self.stdout.write(self.style.WARNING(f"⚠️ No 'entry' found in {file_name}, skipping."))
                continue

            for entry in entry_list:
                changes_list = entry.get('changes', [])
                if not changes_list:
                    self.stdout.write(self.style.WARNING(f"⚠️ No 'changes' in entry of {file_name}, skipping."))
                    continue

                for changes in changes_list:
                    value = changes.get('value', {})
                    contacts = value.get('contacts', [])
                    if not contacts:
                        self.stdout.write(self.style.WARNING(f"⚠️ No 'contacts' in {file_name}, skipping."))
                        continue

                    contact = contacts[0]
                    wa_id = contact.get('wa_id')
                    name = contact.get('profile', {}).get('name', '')

                    # ✅ Handle messages
                    if 'messages' in value:
                        for msg in value['messages']:
                            message_id = msg.get('id')
                            try:
                                timestamp = datetime.fromtimestamp(int(msg.get('timestamp')))
                            except Exception:
                                self.stdout.write(self.style.WARNING(f"⚠️ Invalid timestamp in message {message_id}"))
                                continue

                            text = msg.get('text', {}).get('body', '')
                            status = 'sent'

                            message = Message(
                                wa_id=wa_id,
                                message_id=message_id,
                                timestamp=timestamp,
                                message=text,
                                status=status,
                                user_info={'name': name, 'number': wa_id}
                            )
                            try:
                                message.save()
                                self.stdout.write(self.style.SUCCESS(f"✅ Inserted message {message_id}"))
                            except Exception:
                                self.stdout.write(self.style.WARNING(f"⚠️ Message {message_id} already exists"))

                    # ✅ Handle statuses
                    if 'statuses' in value:
                        for status_payload in value['statuses']:
                            msg_id = status_payload.get('id')
                            status = status_payload.get('status')
                            Message.objects(message_id=msg_id).update_one(set__status=status)
                            self.stdout.write(self.style.SUCCESS(f"🔄 Updated status for {msg_id} → {status}"))

            self.stdout.write(self.style.SUCCESS(f"🎉 Done processing {file_name}"))
