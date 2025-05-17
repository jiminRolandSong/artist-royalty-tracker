from django.core.management.base import BaseCommand
from royalties.models import Artist, RoyaltyRecord, Payment
from datetime import date

class Command(BaseCommand):
    help = "Generate pending payments for artists"

    def handle(self, *args, **kwargs):
        today = date.today()
        artists = Artist.objects.all()

        for artist in artists:
            royalty_records = RoyaltyRecord.objects.filter(track__artist=artist)

            total = 0
            for record in royalty_records:
                payout = record.stream_count * float(record.payout_per_stream)
                total += payout

            if total > 0:
                Payment.objects.create(
                    artist=artist,
                    amount=round(total, 2),
                    status='pending',
                    due_date=today
                )
            royalty_records.update(is_paid=True)

        self.stdout.write(self.style.SUCCESS("Payments successfully generated and royalty records marked as paid."))