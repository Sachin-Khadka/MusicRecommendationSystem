from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView 
from django.views.generic.dates import YearArchiveView
from django.contrib.auth.decorators import login_required
import requests
from ast import literal_eval as make_tuple
import json
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from .models import Music, Rating, Review, Listenlater, History, Channel
from . import  models
from django.db.models import Case, When
from client.models import Music, Listenlater, History, Channel
from django.contrib import messages




# Create your views here.
def client_home(request):
    return render(request, 'client-home-page.html')


class HomeView(ListView):
    model = Music
    template_name = 'client-home-page.html'
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['top_rated'] = Music.objects.filter(status='TR')
        context['most_watched'] = Music.objects.filter(status='MW')
        context['recently_added'] = Music.objects.filter(status='RA')
        print(context)
        return context  


class MusicList(ListView):
    model = Music   
    paginate_by = 10
    template_name = "music_list.html"         
    
class MusicDetail(DetailView):
    model = Music
    template_name = "music_detail.html" 
    def get_object(self):
        object = super(MusicDetail, self).get_object()
        object.views_count += 1
        object.save()
        return object 

    def get_context_data(self, **kwargs):
        context = super(MusicDetail, self).get_context_data(**kwargs)
        context['related_musics'] = Music.objects.filter(category=self.get_object().category)
        print(context)
        return context

     
class MusicCategory(ListView):
    model = Music
    template_name = "music_list.html" 
    paginate_by = 5
     
    def get_queryset(self):
        self.category = self.kwargs['category']
        # musics = Music.objects.filter(category=self.category)
        return Music.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(MusicCategory, self).get_context_data(**kwargs)
        context['music_category'] = self.category
        return context


class MusicLanguage(ListView):
    model = Music
    template_name = "music_list.html" 
    paginate_by = 10 
     
    def get_queryset(self):
        self.language = self.kwargs['lang']
        # musics = Music.objects.filter(category=self.category)
        return Music.objects.filter(language=self.language)

    def get_context_data(self, **kwargs):
        context = super(MusicLanguage, self).get_context_data(**kwargs)
        context['music_language'] = self.language
        return context


class MusicSearch(ListView):
    model = Music
    paginate_by = 100
     
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
            print(query)
            print(object_list)
        else:
            object_list = self.model.objects.none()
        return object_list  


class MusicYear(YearArchiveView):
    queryset  = Music.objects.all()
    date_field ='year_of_production'
    make_object_list = True
    allow_future = True
    print(queryset)


@login_required   
def history(request):
    if request.method == "POST":
        user = request.user
        print("User: ", user)
        music_id = request.POST['music_id']
        print("Music ID: ", music_id)
        print(music_id)
        history = History(user=user, music_id=music_id)
        history.save()
        print(history)
        return redirect("channel.html")
    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    music = Music.objects.filter(music_id__in=ids).order_by(preserved)

    return render(request, 'history.html', {"history": music})


@login_required
def Listenlater(request):
    if request.method == "POST":
        user =  request.user
        print("User Name: ", user)
        video_id = request.POST['video_id']
        print("ID: ", video_id)

        listen = models.Listenlater.objects.filter(user=user)

        for i in listen:
            if video_id == i.video_id:
                message = "Your Music is Already Added"
                messages.success(request, "Your Music is Already Added")
                break
        else:
            listenlater = models.Listenlater(user=user, video_id=video_id)
            listenlater.save()
            message = "Your Music is Succesfully Added"
            messages.success(request, "Your Music is Succesfully Added")

        music = Music.objects.filter(music_id=video_id).first()
        print(music.title)
        return render(request, f"yeah.html", {'music': music, "message": message})


    ll = models.Listenlater.objects.filter(user=request.user)
    ids = []
    for i in ll:
        ids.append(i.video_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    music = Music.objects.filter(music_id__in=ids).order_by(preserved)
    return render(request, "listenlater.html", {'music': music})



def music(request):
    music = Music.objects.all()
    return render(request, 'music.html', {'music': music})


def musicpost(request, id):
    music = Music.objects.filter(music_id=id).first()
    return render(request, 'musicpost.htm', {'music': music})


@login_required
def channel(request, channel):
    chan = Channel.objects.filter(name=channel).first()
    print("Channel: ", chan)
    music_ids = str(chan.music).split(" ")[1:]

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(music_ids)])
    music = Music.objects.filter(music_id__in=music_ids).order_by(preserved)  
    print("Music List: ", music)

    return render(request, "channel.html", {"channel": chan, "music": music})  


@login_required
def upload(request):
    if request.method == "POST":
        title = request.POST['title']
        singer = request.POST['singer']
        band = request.POST['band']
        tag = request.POST['tag']
        year = request.POST['year_production']
        image = request.FILES['picture']
        description = request.POST['description']
        music = request.FILES['file']
       
        music_model = Music(title=title, singer=singer, band=band, cast=tag,  year_of_production = year, image=image, music=music, description=description)
        music_model.save()
        messages.success(request, f'Successfully Added!!')
        music_id = music_model.music_id
        user = request.user 
        print(user)
        channel_find = models.Channel.objects.filter(name=str(request.user))
        print(channel_find)

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()    
    return render(request, "upload.html")


@login_required
def search_function(request):
    if request.method =='POST':
        finds = request.GET['music']
        if finds:
            match = Music.objects.filter(Q(title__icontains=finds))                             
            if match:                
                return render(request,'music_list.html', {'context':match})
            else:
                messages.error(request, "The word, You type did  not Exist")
        else:
            return HttpResponseRedict('music_list.html')  
    return render(request, 'music_list.html')         



def ratingReview(request, mus_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    musics = get_object_or_404(Music, music_id=mus_id)
    # for rating
    if request.method == "POST":

        rate = request.POST['rating'] 
        review = request.POST['review']

        ratingObject = Rating()
        reviewObject = Review()

        ratingObject.user = request.user
        reviewObject.user = request.user

        ratingObject.song = musics
        reviewObject.song = musics

        ratingObject.rating = rate
        reviewObject.review = review

        ratingObject.save()
        reviewObject.save()

        messages.success(request, "Succssfully, Sended Your Rating and Review")
        return redirect("client-home")
    return render(request, 'music_detail.html', {'music': musics})









# @login_required(login_url='login')
# def recommend(request):
#     user_id = request.user.id
#     user_name = request.user.username
#     print("User ID: ", user_id)
#     print("User Name: ", user_name)
#     url = "http://127.0.0.1:8000/recommend/"
#     payload = {'user_id':user_id}
#     headers = {
#         'content-type': "multipart/form-data",
#         'cache-control': "no-cache",
#     }
#     responses = requests.request("POST",url,data=payload)
#     import pdb; pdb.set_trace()
#     response = json.load()
#     print("Response", response)
#     respnses_tuple = make_tuple("Tuple_Response", response)
#     print( respnses_tuple)
#     context = list()
#     print("Context", context)

#     for user_id in respnses_tuple:
#         try:
#             recommended = Music.objects.get(id=user_id)
#             context.append(recommended)
#         except:
#             pass
#     return render(request,"recommend.html",{'context': context})






@login_required(login_url='login')
def recommend(request):
    user_id = request.user.id
    user_name = request.user.username
    print("User ID: ", user_id)
    print("User Name: ", user_name)
    responses = requests.request("POST",url,data=payload)
    response = json.load()
    print("Response", response)
    respnses_tuple = make_tuple("Tuple_Response", response)
    print( respnses_tuple)
    context = list()
    print("Context", context)

    for user_id in respnses_tuple:
        try:
            recommended = Music.objects.get(id=user_id)
            context.append(recommended)
        except:
            pass
    return render(request,"recommend.html",{'context': context})

