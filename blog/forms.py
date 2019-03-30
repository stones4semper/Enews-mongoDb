from django import forms
from .models import Posts, Category

class NewPostForm(forms.ModelForm):    
    class Meta:
        model = Posts
        fields = ['title', 'category', 'content', 'image']


class CatPostForm(forms.ModelForm): 
    class Meta: 
        model=Category
        fields = ['CatName']
