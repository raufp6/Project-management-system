from django.shortcuts import render,HttpResponse

# Create your views here.
from rest_framework import viewsets,filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Task
from project.models import Projects
from notification.models import Notification
from .serializers import TaskSerializer,TaskListSerializer
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView,UpdateAPIView
import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .tasks import test_func
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync
from notification.serializers import NotificationSerializer
# from notifications.signals import notify



def test(request):
    test_func.delay()
    return HttpResponse("Done")

def test_notification(request):
    print("JJJJJJ")
    user = request.user
    print(user.id)
    channel_layer = get_channel_layer()

    last_notification = Notification.objects.order_by('-timestamp').first()

    serializer = NotificationSerializer(last_notification)
    serialized_notification = serializer.data
    
    async_to_sync(channel_layer.group_send)(
        f"notification_63",
        {
            'command':'task_status',
            'type': 'send_notification',
            'message': json.dumps(serialized_notification)
        }
    )
    return HttpResponse("Notification send")




class TaskView(ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = '__all__' 
    search_fields = ['^title','^description']

    def get_queryset(self):
        user = self.request.user
        print(user.is_superuser)
        if user.is_superuser:
            return Task.objects.filter(deleted_at__isnull=True)
        elif user.is_client:
            client_projects = Projects.objects.filter(client__user=user)
            return Task.objects.filter(project__in=client_projects)

        else:
            return Task.objects.filter(deleted_at__isnull=True,assigned_to=user)
    
    def get_serializer_class(self):
        return TaskListSerializer if self.request.method == 'GET' else TaskSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
    # def list(self, request, *args, **kwargs):
    #     # Override list method if needed
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    # serializer_class = TaskListSerializer
    queryset = Task.objects.all()
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'
    
    def get_serializer_class(self):
        return TaskListSerializer if self.request.method == 'GET' else TaskSerializer
    
    def perform_update(self,serializer):
        instance = serializer.save()
        if not self.request.user.is_superuser:
            channel_layer = get_channel_layer()

            last_notification = Notification.objects.order_by('-timestamp').first()

            serializer = NotificationSerializer(last_notification)
            serialized_notification = serializer.data
            
            async_to_sync(channel_layer.group_send)(
                f"notification_{instance.assigned_to}",
                {
                    'command':'task_status',
                    'type': 'send_notification',
                    'message': json.dumps(serialized_notification)
                }
            )
    def perform_destroy(self, instance):
        # Instead of deleting, update the deleted_at field
        instance.deleted_at = datetime.datetime.now().date()  # Make sure to import timezone
        instance.save()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_count(request):
    user = request.user
    status = request.GET.get('status')
    if user.is_superuser:
        if status:
            count = Task.objects.filter(deleted_at__isnull=True,status=status).count()
        else:
            count = Task.objects.filter(deleted_at__isnull=True).count()
    elif user.is_client:
        client_projects = Projects.objects.filter(client__user=user)
        if status:
            count = Task.objects.filter(project__in=client_projects,status=status).count()
        else:
            count = Task.objects.filter(project__in=client_projects).count()

    else:
        if status:
            count = Task.objects.filter(deleted_at__isnull=True,assigned_to=user,status=status).count()
        else:
            count = Task.objects.filter(deleted_at__isnull=True,assigned_to=user).count()
    
    
    return Response({'count':count})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    user = request.user
    notifications = Notification.objects.unread().filter(recipient=user).all()
    # Serialize the notifications using a serializer
    serializer = NotificationSerializer(notifications, many=True)
    serialized_notifications = serializer.data
    
    return Response(serialized_notifications)