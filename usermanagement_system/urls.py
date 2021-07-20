from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('home.urls')),
    path('', include('signin_signup.urls')),
    path('', include('my_account.urls')),
    path('', include('dashboard.urls')),
    path('', include('client.urls')),
    path('', include('matrixfactorization.urls')),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)