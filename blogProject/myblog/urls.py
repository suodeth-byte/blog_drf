from django.urls import path
from .views import HomeView, ArticleCreateView, SignUpView, LoginView, LogOutView, hello_world, ArticleDetailView, ArticleListView

urlpatterns = [
    path('hello/', hello_world, name='hello'),
    path('', HomeView.as_view(), name='home'),
    path('list/', ArticleListView.as_view(), name='list'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('update/<int:pk>/', ArticleDetailView.as_view(), name='article-update'),
    path('signup/', SignUpView, name='sign-up'),
    path('login/', LoginView, name='login'),
    path('logout/', LogOutView, name='logout'),
    # path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    # path('add_article/', ArticleCreateView, name='article-create')

]
