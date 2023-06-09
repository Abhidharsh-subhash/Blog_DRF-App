from rest_framework.test import APITestCase,APIRequestFactory
from .views import PostListCreateView
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User=get_user_model()
class HelloWorldTestCase(APITestCase):
    def test_helllo_world(self):
        response=self.client.get(reverse('posts_home'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data["message"],"Hello Restframework not post")

class PostListCreateTestCase(APITestCase):
    def setUp(self):
        # self.factory=APIRequestFactory()
        # self.view=PostListCreateView.as_view()
        self.url=reverse('list_posts')
        # this has been created to test the api's that needed authentication to perform
        # self.user=User.objects.create(username='ajay',email='ajay@gmail.com',password='ajay@123')
    def authenticate(self):
        self.client.post(
            reverse('signup'),
            {
                'email':'manu@gmail.com',
                'password':'manu@123',
                'username':'manu'
            },
        )
        response=self.client.post(
            reverse('login'),
            {
                'email':'manu@gmail.com',
                'password':'manu@123'
            },
        )
        print(response.data)
    def test_list_posts(self):
        # request=self.factory.get(self.url)
        response=self.client.get(self.url)
        # response=self.view(request)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['count'],0)
        self.assertEqual(response.data['results'],[])
    def test_post_creation(self):
        # test_post={
        #     'title':'test post',
        #     'content':'test content',
        # }
        # request=self.factory.post(self.url,test_post)
        # request.user=self.user
        # response=self.view(request)
        # self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.authenticate()
