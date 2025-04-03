from django import forms
from .models import User, TravelPost, Review, Location

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['username', 'name', 'password']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.lower()

class TravelPostForm(forms.ModelForm):
    class Meta:
        model = TravelPost
        fields = ['title', 'content', 'image', 'location']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location_name', 'location_id', 'district', 
                 'nearest_railway_station', 'distance_from_railway_station',
                 'nearest_airport', 'distance_from_airport']
        
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    search_type = forms.ChoiceField(
        choices=[
            ('all', 'All'),
            ('users', 'Users'),
            ('posts', 'Posts'),
            ('locations', 'Locations')
        ],
        initial='all',
        required=True
    )