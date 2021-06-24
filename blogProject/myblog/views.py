from django_filters import filters
from django.shortcuts import redirect, render
from rest_framework.generics import get_object_or_404

from .models import Post
from .serializers import PostSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from .pagination import HomePagination
from rest_framework.views import APIView
from rest_framework import generics, status, mixins
from .pagination import HomePagination, HomeLimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PostFilter, IsOwnerFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import PostCreatePermission
from .forms import CreateUserForm
from django.contrib.auth.models import User, Group
from .decorators import unauthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect


@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})


# @api_view(['GET'])
# def Home(request):
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         # content = {'please move along': 'nothing to see here'}
#         # return JsonResponse(content, status=status.HTTP_200_OK)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class HomeView(generics.ListAPIView, mixins.CreateModelMixin):
    queryset = Post.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HomePagination
    # filter_backends = [DjangoFilterBackend]
    # template_name = 'home.html'
    # filterset_class = PostFilter
    # filterset_class = IsOwnerFilterBackend
###########################################################

    # filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'content']
    # ordering_fields = ['date_created']
    #########################################################

    # filterset_fields = ['title']
    # pagination_class = HomeLimitOffsetPagination

    def get_queryset(self):
        # user = self.request.user
        posts = User.objects.all()
        return posts


class ArticleListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HomePagination

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(author=user)
        return posts


class ArticleCreateView(generics.ListCreateAPIView, mixins.CreateModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostCreatePermission]
    pagination_class = HomePagination

    def get_queryset(self):
        owner = self.request.user
        posts = Post.objects.filter(author=owner)
        return posts

    # def list(self, request):
    #     # Note the use of `get_queryset()` instead of `self.queryset`
    #     queryset = self.get_queryset()
    #     serializer = PostSerializer(queryset, many=True)
    #     return Response(serializer.data)


    # def create(self, request, *args, **kwargs):
    #     print(self.request.data.get('author'))
    #     author = self.request.user
    #     title = self.request.data.get('title')
    #     content = self.request.data.get('content')
    #     serializer_class = self.serializer_class
    #     serializer = serializer_class(data={'title': title, 'author': author, 'content': content})
    #     if serializer.is_valid():
    #         print("True")
    #         serializer.save()
    #     else:
    #         print("FALSE")
    #         return Response(serializer.errors)
    #     Post.objects.create(serializer.validated_data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView, mixins.RetrieveModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostCreatePermission]
    pagination_class = HomePagination
    filter_backends = [IsOwnerFilterBackend]
    # lookup_url_kwarg = 'id'
    # filterset_class = PostFilter

    lookup_field = 'post_id'
    # lookup_url_kwarg = 'pk'

    # def get_queryset(self):
    #     # post_id = self.kwargs['id']
    #     queryset = Post.objects.all()
    #     current_user_post = queryset.filter(author=self.request.user)
    #     return current_user_post
        # return Post.objects.filter(id=post_id)

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, id=self.request.data.get('post_id'))
    #     return obj

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, id=self.lookup_url_kwarg)

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, id=self.lookup_url_kwarg)
    #
    #     return obj
    #
    # def get(self, request, *args, **kwargs):
    #     return self.get_object()


@unauthenticated
def SignUpView(request):
    form = CreateUserForm({})
    print(form.is_bound)
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            # form.save()
            username = form.data.get('username')
            email = form.data.get('email')
            password = form.data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'sign_up.html', context)


@unauthenticated
def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("IsAuthenticated", user.is_authenticated)
            messages.info(request, 'Username or Password is incorrect')
            return redirect('home')

    context = {}
    return render(request, 'login.html', context)


def LogOutView(request):
    logout(request)
    return redirect('login')
