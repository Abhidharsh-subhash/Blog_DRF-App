from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,APIView
from .models import Post
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404

@api_view(http_method_names=['GET','POST'])
def homepage(request:Request):
    if request.method == 'POST':
        data=request.data
        response={"message":"Hello Restframework post","data":data}
        return Response(data=response,status=status.HTTP_201_CREATED)
    response={"message":"Hello Restframework not post"}
    return Response(data=response,status=status.HTTP_200_OK)

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

class PostListCreateView(APIView):
    """
    a view for creating and listing posts
    """
    #it allow us to convert our object to json as well as be able to create post request with some validations
    serializer_class=PostSerializer
    def get(self,request:Request,*args,**kwargs):
        posts=Post.objects.all()
        #creating an instance of our serializer that going to help us serilize the posts
        serializer=self.serializer_class(instance=posts,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request:Request,*args,**kwargs):
        data=request.data
        serializer=self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response={
                'message':'Post created',
                'data':serializer.data
            }
            return Response(data=response,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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

class PostRetrieveUpdateDeleteView(APIView):
    serialzer_class=PostSerializer
    def get(self,request:Request,post_id:int):
        post=get_object_or_404(Post,pk=post_id)
        serializer=self.serialzer_class(instance=post)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def put(self,request:Request,post_id:int):
        post=get_object_or_404(Post,pk=post_id)
        data=request.data
        serializer=self.serialzer_class(instance=post,data=data)
        if serializer.is_valid():
            serializer.save()
            response={
                'message':'Post updated',
                'data':serializer.data
            }
            return Response(data=response,status=status.HTTP_200_OK)
        return response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request:Request,post_id:int):
        post=get_object_or_404(Post,pk=post_id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



