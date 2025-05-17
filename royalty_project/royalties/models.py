from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    agency = models.CharField(max_length=100, blank=True)
    join_date = models.DateField()
    
    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in seconds")
    
    def __str__(self):
        return self.title

class RoyaltyRecord(models.Model):
    PLATFORM_CHOICES = [
        ("spotify", "Spotify"),
        ("apple", "Apple Music"),
        ("youTube", "YouTube"),
    ]
    
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    stream_date = models.DateField()
    stream_count = models.PositiveIntegerField()
    payout_per_stream = models.DecimalField(max_digits=10, decimal_places=6)
    is_paid = models.BooleanField(default=False) 
    
    def total_payout(self):
        return self.stream_count * self.payout_per_stream

    def __str__(self):
        return f"{self.track.title} - {self.platform} - {self.stream_date}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
    ]

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.artist.name} - {self.amount} ({self.status})"
