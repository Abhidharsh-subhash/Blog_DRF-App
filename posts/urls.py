from . import views
from django.urls import path

urlpatterns = [
    path("homepage/",views.homepage,name='posts_home'),
    #ignored when we uses routers
    path('',views.PostListCreateView.as_view(),name='list_posts'),
    path('<int:pk>/',views.PostRetrieveUpdateDeleteView.as_view(),name='post_detial'),
]