from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from .models import Posts, Category
from .forms import CatPostForm, NewPostForm
from django.views.generic import (
    ListView, 
    DetailView, 
    UpdateView,
    CreateView,
    DeleteView,
    TemplateView
)

pagNum = 1

def about(request):
    return render(request, 'blog/about.html', {})

class UserPostListView(ListView):
    model = Posts
    template_name = 'blog/UserPosts.html'
    context_object_name = 'posts'
    paginate_by = pagNum

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')

class CatPostListView(ListView):
    model = Posts
    template_name = 'blog/CatPosts.html'
    context_object_name = 'posts'
    paginate_by = pagNum

    def get_queryset(self):
        DeyId = get_object_or_404(Category, CatName=self.kwargs.get('category'))  
        return Posts.objects.filter(category_id=DeyId).order_by('-date_posted') 

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

@login_required
def newPost(request):    
    deyCat = Category.objects.all() 
    if request.method =='POST':
        myForm = NewPostForm(request.POST, request.FILES)
        response_data = {
            'SType': 'danger',
            'message': "An Error Occured, pls try again later"
        }
        if request.POST.get('deyHidden') == 'create_hidden':
            title = request.POST.get('title')
            content = request.POST.get('content')
            category_id = request.POST.get('category')
            image = request.FILES.get('image') 
            if myForm.is_valid():
                if Posts.objects.create(title=title, content=content, category_id=category_id, image=image, author_id=request.user.id):
                    response_data = {
                        'SType': 'success',
                        'message': "Saved Successfully"
                    }   
            return HttpResponse(json.dumps(response_data), content_type="application/json")  
        elif request.POST.get('deyHidden') == 'category_hidden':
            CatNames = request.POST.getlist('CatName[]')
            for CatName in CatNames:
                Category.objects.get_or_create(CatName=CatName)
            response_data = {
                'SType': 'success',
                'message': "Saved Successfully"
            }                
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    context={
        'form':NewPostForm(),
        'title':'Create Post',
        'category': Category.objects.all()
    }
    return render(request, 'blog/form.html', context)

@login_required
def UpdatePost(request, pk):
    obj = get_object_or_404(Posts, id=pk)
    myForm = NewPostForm(instance = obj)
    if request.method == 'POST':
        myForm = NewPostForm(request.POST, request.FILES, instance=obj)
        response_data = {
            'SType': 'danger',
            'message': "An Error Occured, pls try again later"
        }
        if myForm.is_valid():
            if myForm.save():
                response_data = {
                    'SType': 'success',
                    'message': "Updated Successfully"
                } 
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    context={ 
        'form':myForm,
        'title': obj.title,
        'category': Category.objects.all()
    }
    return render(request, 'blog/update.html', context) 

def PostDetail(request, pk):
    obj = get_object_or_404(Posts, id=pk)
    nextPost = Posts.objects.filter(id__gt=obj.id).order_by('id').first()
    prevPost = Posts.objects.filter(id__lt=obj.id).order_by('-id').first()
    context={ 
        'object':obj,
        'title': obj.title,
        'nextPost': nextPost,
        'prevPost': prevPost,
        'latests': Posts.objects.all().order_by('-id')[:5]
    }
    return render(request, 'blog/details.html', context) 

def index(request):
    posts_list = Posts.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(posts_list, pagNum)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/home.html', { 'posts': posts })

class NewPostView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/form.html'
    deyCat = Category.objects.all()

    def get(self, request, **kwargs):
        context = {
            'form': NewPostForm(),
            'title': 'Create Post',
            'categories': self.deyCat
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        myForm = NewPostForm(request.POST, request.FILES)
        response_data = {
            'SType': 'danger',
            'message': "An Error Occured, pls try again later"
        }
        if request.POST.get('deyHidden') == 'create_hidden':
            title = request.POST.get('title')
            content = request.POST.get('content')
            category_id = request.POST.get('category')
            image = request.FILES.get('image')
            if myForm.is_valid():
                if Posts.objects.create(title=title, content=content, category_id=category_id, image=image,
                                        author_id=request.user.id):
                    response_data = {
                        'SType': 'success',
                        'message': "Saved Successfully"
                    }
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif request.POST.get('deyHidden') == 'category_hidden':
            CatNames = request.POST.getlist('CatName[]')
            for CatName in CatNames:
                Category.objects.get_or_create(CatName=CatName)
            response_data = {
                'SType': 'success',
                'message': "Saved Successfully"
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json")