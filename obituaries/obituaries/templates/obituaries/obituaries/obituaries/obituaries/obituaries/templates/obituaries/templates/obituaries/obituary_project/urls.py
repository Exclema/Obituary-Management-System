from django.contrib import admin
from django.urls import path
from django.contrib.sitemaps.views import sitemap
from obituaries.sitemaps import ObituarySitemap
from obituaries import views

sitemaps = {
    'obituaries': ObituarySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('submit/', views.submit_obituary, name='submit_obituary'),
    path('obituaries/', views.view_obituaries, name='view_obituaries'),
    path('obituary/<slug:slug>/', views.ObituaryDetailView.as_view(), name='obituary_detail'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
