from django.db import models
from django.contrib.auth.models import User


class Albumtable(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=60)
    album_year = models.IntegerField(null=True)

    def __int__(self):
        return self.album_name


class Songstable(models.Model):
    song_id = models.AutoField(primary_key=True)
    album_id = models.ForeignKey(Albumtable, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=60)
    artist_name = models.CharField(max_length=60)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.song_name


class Ratingtable(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    song_id = models.ForeignKey(Songstable, on_delete=models.CASCADE)
    user_rating = models.IntegerField(null=True)

    def __str__(self):
        return '%s %s' % (self.song_id, self.user_rating)



