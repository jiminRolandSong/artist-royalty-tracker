from django.test import TestCase
from royalties.models import Artist, Track, RoyaltyRecord, Payment
from django.utils import timezone
from django.urls import reverse
from django.core.management import call_command

# Create your tests here.

class PaymentGenerationTest(TestCase):
    def setUp(self):
        # Setup artist, track, and unpaid royalty records
        self.artist = Artist.objects.create(name="Command Artist", genre="EDM", agency="X", join_date=timezone.now())
        self.track = Track.objects.create(title="Command Track", artist=self.artist, release_date=timezone.now(), duration=180)

        for _ in range(2):
            RoyaltyRecord.objects.create(
                track=self.track,
                platform="Spotify",
                stream_date=timezone.now(),
                stream_count=1000,
                payout_per_stream=0.005,
                is_paid=False
            )

    def test_generate_payments(self):
        self.assertEqual(Payment.objects.count(), 0)

        call_command('generate_payments')

        # Payment should now exist
        self.assertEqual(Payment.objects.count(), 1)

        payment = Payment.objects.first()
        self.assertEqual(float(payment.amount), 10.00)  # 2 * 1000 * 0.005
        self.assertEqual(payment.artist, self.artist)

        # Check RoyaltyRecords are marked as paid
        unpaid = RoyaltyRecord.objects.filter(is_paid=False)
        self.assertEqual(unpaid.count(), 0)


class MarkPaymentAsPaidTest(TestCase):
    def setUp(self):
        # Setup artist and track
        self.artist = Artist.objects.create(name="API Artist", genre="EDM", agency="X", join_date=timezone.now())
        self.track = Track.objects.create(title="Test Track", artist=self.artist, release_date=timezone.now(), duration=200)

        # Create RoyaltyRecords 
        royalty = RoyaltyRecord.objects.create(
            track=self.track,
            platform="Spotify",
            stream_date=timezone.now(),
            stream_count=2000,
            payout_per_stream=0.004,
            is_paid=False
        )

        # Create a pending payment
        self.payment = Payment.objects.create(
            artist=self.artist,
            amount=8.00,
            status="pending",
            due_date=timezone.now().date(),
            paid_date=None
        )

    def test_mark_paid_api(self):
        url = reverse('mark_paid', args=[self.payment.id])
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 200)
        self.payment.refresh_from_db()

        self.assertEqual(self.payment.status, "paid")
        self.assertIsNotNone(self.payment.paid_date)

