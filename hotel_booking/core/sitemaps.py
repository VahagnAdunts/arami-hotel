from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Room

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['home', 'rooms', 'check_availability']

    def location(self, item):
        return reverse(item)

class RoomSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Room.objects.all()

    def location(self, obj):
        return reverse('room_detail', args=[obj.type]) 