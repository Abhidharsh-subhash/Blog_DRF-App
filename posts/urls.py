from . import views
from django.urls import path

urlpatterns = [
    path("homepage/",views.homepage,name='posts_home'),
    path('',views.list_posts,name='list_posts'),
    path('<int:post_id>',views.post_detial,name='post_detial'),
    path('update/<int:post_id>/',views.update_post,name='update_post'),
    path('getpost<int:post_id>/',views.get_post_by_id,name='getpost')
]