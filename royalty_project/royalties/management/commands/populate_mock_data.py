import random
from datetime import timedelta, date
from django.core.management.base import BaseCommand
from royalties.models import Artist, Track, RoyaltyRecord

class Command(BaseCommand):
    help = "Polulate database with mock royalty data"
    
    def handle(self, *args, **kwargs):
        platform_choices = ["spotify", "apple", "youtube"]
        base_date = date.today() - timedelta(days=180)
        
        artists = []
        artist_names = ["Andrew Romane", "Bob Holywater", "Craig Xavier", "Daniel Serenade", "Ethan Aspen"]
        for i in range(5):
            artist = Artist.objects.create(
                name = artist_names[i],
                genre = random.choice(["House", "Techno", "Mainstage"]),
                agency = "Agency TUE",
                join_date=base_date - timedelta(days=random.randint(100, 1000)),
                )
            artists.append(artist)
        
        tracks = []
        for artist in artists:
            for j in range(random.randint(2, 3)):
                track = Track.objects.create(
                    title=f"{artist.name}'s Track {j+1}",
                    artist=artist,
                    release_date=base_date - timedelta(days=random.randint(30, 200)),
                    duration=random.randint(150, 300),
                )
                tracks.append(track)

        for track in tracks:
            for i in range(20):  # 20 records per track
                RoyaltyRecord.objects.create(
                    track=track,
                    platform=random.choice(platform_choices),
                    stream_date=base_date + timedelta(days=random.randint(0, 180)),
                    stream_count=random.randint(1000, 100000),
                    payout_per_stream=round(random.uniform(0.002, 0.006), 6),
                )

        self.stdout.write(self.style.SUCCESS("Mock data successfully created!"))