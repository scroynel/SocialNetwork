from django.http import JsonResponse

from account.models import User
from account.serializers import UserSerializer

from post.models import Post
from post.serializers import PostSerializer

from rest_framework.decorators import api_view, authentication_classes, permission_classes

@api_view(['POST'])
def search(request):
    query = request.data['query']

    users = User.objects.filter(name__icontains = query)
    users_serializer = UserSerializer(users, many=True)

    posts = Post.objects.filter(body__icontains = query)
    posts_serializer = PostSerializer(posts, many=True)

    return JsonResponse({
        'users': users_serializer.data,
        'posts': posts_serializer.data
        }, safe=False)