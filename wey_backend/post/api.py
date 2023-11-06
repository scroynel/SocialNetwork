from django.shortcuts import render
from django.http import JsonResponse

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from notification.utils import create_notification

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, Trend
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer

#  I'll see my posts and posts of my friends
@api_view(['GET'])
def post_list(request):
    user_ids = [str(request.user.id), ]
    user_ids.append(str(request.user.id))

    for friend in request.user.friends.all():
        user_ids.append(str(friend.id))

    posts = Post.objects.filter(created_by_id__in=user_ids)

    trend = request.GET.get('trend', '')
    if trend:
        posts = posts.filter(body__icontains = trend)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)

    serializer = PostDetailSerializer(post)

    return JsonResponse({
        'post': serializer.data
    })


@api_view(['GET'])
def post_list_profile(request, pk):
    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(created_by_id = pk)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False

    check1 = FriendshipRequest.objects.filter(created_for = request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for = user).filter(created_by = request.user)

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        'can_send_friendship_request': can_send_friendship_request
    }, safe=False)

    

@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)
    
    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        request_user = request.user
        request_user.posts_count += 1
        request_user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:  
        return JsonResponse({'error': 'Something went wrong with add post!'})
    

@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by = request.user):

        like = Like.objects.create(created_by = request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count += 1
        post.likes.add(like)
        post.save()

        notification = create_notification(request, 'post_like', post_id = post.id)

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})

    
@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body = request.data.get('body'), created_by = request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    notification = create_notification(request, 'post_comment', post_id = post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()

    serializer = TrendSerializer(trends, many=True)

    return JsonResponse(serializer.data, safe=False)