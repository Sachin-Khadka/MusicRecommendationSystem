from .models import Music

def slider_musics(request):
    musics = Music.objects.all().order_by('created')[0:4]
    return { 'slider_musics': musics }