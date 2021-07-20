from django.db import models
from django.db import models
from django.contrib.auth.models import Permission, User
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


# Create your models here.

CATEGORY_COICES = (
    ('pop', 'POP'), 
    ('funk', 'FUNK'), 
    ('classical', 'CLASSICAL'), 
    ('rock', 'ROCK'), 
    ('country', 'COUNTRY'), 
    ('hiphop', 'HIPHOP'), 
    ('jazz', 'JAZZ'), 
    ('folk', 'FOLK'),
    ('rap', 'RAP'), 
    ('metal', 'METAL'), 
)

LANGUAGE_COICES = (
    ('english', 'ENGLISH'), 
    ('nepali', 'NEPALI'),  
    ('hindi', 'HINDI'),  
)


STATUS_COICES = (
    ('RA', 'RECENTLY ADDED'), 
    ('MW', 'MOST WATCHED'), 
    ('TR', 'TOP RATED'), 
)

        
# Create your models here.
class Playlist(models.Model):
        image = models.ImageField(upload_to="playlist_images")
        playlistName = models.CharField(max_length=2000)
        description = models.CharField(max_length=2000)


#create categories modal or playlist
class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __str__ (self):
        return self.title        

class Music(models.Model):
    music_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="muisc_images")
    singer = models.CharField(max_length=2000)
    band = models.CharField(max_length=2000)
    banner = models.ImageField(upload_to="music_banner")
    music = models.FileField(upload_to='musics')
    category = models.CharField(choices=CATEGORY_COICES,max_length=10)
    language = models.CharField(choices=LANGUAGE_COICES,  max_length=10)
    status = models.CharField(choices=STATUS_COICES, max_length=2)
    cast = models.CharField(max_length=100) 
    year_of_production = models.DateField()
    views_count = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.now())
    updated = models.DateTimeField(default=datetime.now())
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args,**kwargs):
        if not self.slug :
            self.slug = slugify(self.title)
        super(Music, self).save(*args,**kwargs)

    def __str__(self):
        return self.title 
   
class Listenlater(models.Model):
    listen_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=10000000)

class History(models.Model):
    hist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music_id = models.CharField(max_length=10000000)

class Channel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    music = models.CharField(max_length=100000000) 
    def __str__(self):
        return self.name + " Channel"  

class Rating(models.Model):
	user   	= models.ForeignKey(User,on_delete=models.CASCADE)
	song 	= models.ForeignKey(Music,on_delete=models.CASCADE)
	rating 	= models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])

class Review(models.Model):
	user   	= models.ForeignKey(User,on_delete=models.CASCADE)
	song 	= models.ForeignKey(Music,on_delete=models.CASCADE)
	review 	= models.CharField(max_length=250)













# class Cluster(models.Model):
#     name = models.CharField(max_length=100)
#     users = models.ManyToManyField(User)
#     def get_members(self):
#         return "\n".join([u.username for u in self.users.all()])



  
