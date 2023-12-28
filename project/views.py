from rest_framework import viewsets,authentication,filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Client,Projects,CustomUser
from .serializers import ProjectSerializer,ProjectListSerializer
from rest_framework.generics import  ListCreateAPIView, RetrieveUpdateDestroyAPIView,UpdateAPIView
import datetime
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffPermission
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import PageNumberPagination


# class LargeResultsSetPagination(PageNumberPagination):
#     page_size = 1000
#     page_size_query_param = 'page_size'
#     max_page_size = 10000
    

class ProjectView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    # authentication_classes = [authentication.SessionAuthentication]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = '__all__' 
    search_fields = ['^name','^description']
    permission_classes = [IsStaffPermission]
    # pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Projects.objects.filter(deleted_at__isnull=True)
        elif user.is_client:
            client = Client.objects.filter(user=user).first()
            return Projects.objects.filter(deleted_at__isnull=True,client=client.id)
        else:
            return Projects.objects.filter(deleted_at__isnull=True)


    
    def get_serializer_class(self):
        # Use ProjectListSerializer for list action
        return ProjectListSerializer if self.request.method == 'GET' else ProjectSerializer

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


class ProjectRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Projects.objects.all()
    # authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [IsStaffPermission]
    lookup_field = 'pk'

    def get_serializer_class(self):
        # Use ProjectListSerializer for list action
        return ProjectListSerializer if self.request.method == 'GET' else ProjectSerializer
    def perform_destroy(self, instance):
        # Instead of deleting, update the deleted_at field
        instance.deleted_at = datetime.datetime.now().date()  # Make sure to import timezone
        instance.save()

# @api_view(["GET"])
# def project_count(request,*args, **kwargs):
#     count = Projects.objects.count()
#     return Response({"message":"Hello world"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def project_count(request):
    user = request.user
    if user.is_superuser:
        count = Projects.objects.filter(deleted_at__isnull=True).count()
    elif user.is_client:
        client = Client.objects.filter(user=user).first()
        count = Projects.objects.filter(deleted_at__isnull=True,client=client.id).count()
    else:
        count = Projects.objects.filter(deleted_at__isnull=True).count()
    
    
    return Response({'count':count})