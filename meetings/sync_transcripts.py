from django.core.management.base import BaseCommand
from .models import Transcript
from .clients import FirefliesClient

class Command(BaseCommand):
    help = 'Sync transcripts from Fireflies'

    def handle(self, *args, **kwargs):
        fireflies_client = FirefliesClient()
        data = fireflies_client.get_transcripts()
        for item in data.get('transcripts', []):
            transcript, created = Transcript.objects.update_or_create(
                meeting_id=item['id'],
                defaults={
                    'source': 'Fireflies',
                    'title': item['title'],
                    'content': item['content'],
                    'recorded_at': item['recorded_at'],
                }
            )
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'{action} transcript: {transcript.title}')