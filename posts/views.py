from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework import status,mixins
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.generics import GenericAPIView
from .models import Post
from .serializers import PostSerializer
from .permissions import ReadOnly,AuthorOrReadonly
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
#when dealing with viewsets
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema

#custom class for defining the pagination class
class CustomPaginator(PageNumberPagination):
    page_size=4
    page_query_param='page'
    page_size_query_param='page_size'

@api_view(http_method_names=['GET','POST'])
@permission_classes([AllowAny])
def homepage(request:Request):
    if request.method == 'POST':
        data=request.data
        response={"message":"Hello Restframework post","data":data}
        return Response(data=response,status=status.HTTP_201_CREATED)
    response={"message":"Hello Restframework not post"}
    return Response(data=response,status=status.HTTP_200_OK)

#Creating function based views
# @api_view(http_method_names=['GET','POST'])
# def list_posts(request:Request):
#     posts=Post.objects.all() 
#     if request.method == 'POST':
#         #data as json
#         data=request.data
#         serializer=PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response={
#                 'message':'Post Created',
#                 'data':serializer.data
#             }
#             return Response(data=response,status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     #instance is actually the data that we want to return as json and many=True because it is query set
#     serializer=PostSerializer(instance=posts,many=True)
#     response={
#         'message':'posts',
#         'data':serializer.data
#     }
#     return Response(data=response,status=status.HTTP_200_OK)

#Creating class based views with APIView
# class PostListCreateView(APIView):
#     """
#     a view for creating and listing posts
#     """
#     #it allow us to convert our object to json as well as be able to create post request with some validations
#     serializer_class=PostSerializer
#     permission_classes=[IsAuthenticatedOrReadOnly]
#     def get(self,request:Request,*args,**kwargs):
#         posts=Post.objects.all()
#         #creating an instance of our serializer that going to help us serilize the posts
#         serializer=self.serializer_class(instance=posts,many=True)
#         return Response(data=serializer.data,status=status.HTTP_200_OK)
#     def post(self,request:Request,*args,**kwargs):
#         data=request.data
#         serializer=self.serializer_class(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response={
#                 'message':'Post created',
#                 'data':serializer.data
#             }
#             return Response(data=response,status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#Creating views using GenericAPIView with mixins
class PostListCreateView(GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
    serializer_class=PostSerializer
    #while testing this code in test.py file then you need to change the permission to allowany
    permission_classes=[IsAuthenticated]
    # permission_classes=[IsAuthenticated]
    pagination_class=CustomPaginator
    queryset=Post.objects.all()
    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)
    @swagger_auto_schema(
            operation_summary='lists of all posts available',
            operation_description='This returns list of all posts'
    )
    def get(self,request:Request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def post(self,request:Request,*args,**kwargs):
        return self.create(request,*args,**kwargs)

# @api_view(http_method_names=['GET'])
# def post_detial(request:Request,post_id:int):
#     post = get_object_or_404(Post,pk=post_id)
#     serializer=PostSerializer(instance=post)
#     response={
#         'message':'post',
#         'data':serializer.data
#     }
#     return Response(data=response,status=status.HTTP_200_OK)

# @api_view(http_method_names=['GET'])
# def get_post_by_id(request:Request,post_id=int):
#     post = get_object_or_404(Post,pk=post_id)
#     serializer=PostSerializer(instance=post)
#     if serializer.is_valid():
#         serializer.save()
#         response={
#             'message':'post',
#             'data':serializer.data
#         }
#         return Response(data=response,status=status.HTTP_200_OK)

# @api_view(http_method_names=['PUT'])
# def update_post(request:Request,post_id=int):
#     post = get_object_or_404(Post,pk=post_id)
#     data=request.data
#     serializer=PostSerializer(instance=post,data=data)
#     if serializer.is_valid():
#         serializer.save()
#         response={
#             'message':'Post updated successfully',
#             'data':serializer.data
#         }
#         return Response(data=response,status=status.HTTP_200_OK)
#     return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(http_method_names=['DELETE'])
# def delete_post(request:Request,post_id=int):
#     post=get_object_or_404(Post,pk=post_id)
#     post.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

# class PostRetrieveUpdateDeleteView(APIView):
#     serialzer_class=PostSerializer
#     def get(self,request:Request,post_id:int):
#         post=get_object_or_404(Post,pk=post_id)
#         serializer=self.serialzer_class(instance=post)
#         return Response(data=serializer.data,status=status.HTTP_200_OK)
#     def put(self,request:Request,post_id:int):
#         post=get_object_or_404(Post,pk=post_id)
#         data=request.data
#         serializer=self.serialzer_class(instance=post,data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response={
#                 'message':'Post updated',
#                 'data':serializer.data
#             }
#             return Response(data=response,status=status.HTTP_200_OK)
#         return response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request:Request,post_id:int):
#         post=get_object_or_404(Post,pk=post_id)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class PostRetrieveUpdateDeleteView(GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class=PostSerializer
    queryset=Post.objects.all()
    permission_classes=[AuthorOrReadonly]
    def get(self,request:Request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request:Request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    def delete(self,request:Request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

# class PostViewset(viewsets.ViewSet):
#     def list(self,request:Request):
#         queryset=Post.objects.all()
#         serializer=PostSerializer(instance=queryset,many=True)
#         return Response(data=serializer.data,status=status.HTTP_200_OK)
#     def retrieve(self,request:Request,pk=None):
#         post=get_object_or_404(Post,pk=pk)
#         serializer=PostSerializer(instance=post)
#         return Response(data=serializer.data,status=status.HTTP_200_OK)

#with this function we can perform all the crud operations with viewsets
# class PostViewset(viewsets.ModelViewSet):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer

class ListPostsForAuthor(GenericAPIView,mixins.ListModelMixin):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):

        # this is used when we fetch the posts in accordance with the user
        # user=self.request.user
        # this is used when we directly give the username with the request
        # username=self.kwargs.get('username')
        username=self.request.query_params.get('username') or None
        queryset=Post.objects.all()
        if username is not None:
            #it is we are using author__ is know as lookup
            return Post.objects.filter(author__username=username)
        return queryset

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)