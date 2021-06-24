from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view
from django.views.generic import DetailView, ListView, CreateView
from .models import *
from .serializers import PostSerializer
from . forms import PostForm
from rest_framework.pagination import PageNumberPagination


def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'home.html', context)


class HomeView(generics.ListAPIView, mixins.ListModelMixin):
    pagination_class = PageNumberPagination
    page_size = 1

    # renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        queryset = Post.objects.all()
        posts = [post for post in queryset]
        context = {'posts': posts}
        return Response(context)


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
    # renderer_classes = [TemplateHTMLRenderer]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # here the object is retrieved
        serializer = self.get_serializer(instance)
        context = {'post': serializer.data}
        return Response(context, template_name='article_detail.html')


@csrf_exempt
# @api_view(['POST', 'GET'])
def ArticleCreateView(request):

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            # form = PostSerializer(form)
            return reverse('myblog:article-detail', request)
    context = {'form': form}
    return render(request, template_name='add_article.html', context=context)


# class ArticleCreateView(CreateView):
#     model = Post
#     template_name = 'add_article.html'
#     fields = '__all__'
