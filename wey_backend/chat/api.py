from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User

from .models import Conversation, ConversationMessages
from .serializers import ConversationSerializer, ConversationDetailSerialializer, ConversationMessageSerializer

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in = [request.user])
    

    serializer = ConversationSerializer(conversations, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in = [request.user]).get(pk=pk)

    serializer = ConversationDetailSerialializer(conversation)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get_or_create(request, pk):
    user = User.objects.get(pk=pk)

    conversations = Conversation.objects.filter(users__in = [request.user]).filter(users__in = [user])

    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    serializer = ConversationDetailSerialializer(conversation)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in = [request.user]).get(pk=pk)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conversation_message = ConversationMessages.objects.create(
        conversation = conversation,
        body = request.data.get('body'),
        created_by = request.user,
        sent_to = sent_to
    )

    serializer = ConversationMessageSerializer(conversation_message)

    return JsonResponse(serializer.data, safe = False)