from django.contrib import admin
from .models import User, TravelPost, Review, Location

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'is_admin', 'is_active')
    search_fields = ('username', 'name')
    list_filter = ('is_admin', 'is_active')

@admin.register(TravelPost)
class TravelPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'location', 'posted')
    search_fields = ('title', 'content')
    list_filter = ('posted', 'location')
    date_hierarchy = 'posted'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'travel_post', 'rating', 'posted')
    search_fields = ('comment',)
    list_filter = ('rating', 'posted')
    date_hierarchy = 'posted'

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_id', 'district', 'nearest_railway_station')
    search_fields = ('location_name', 'district', 'nearest_railway_station', 'nearest_airport')
    list_filter = ('district',)
