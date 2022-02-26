from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from .models import Task, STATUS_CHOICES, TaskHistory
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend,FilterSet,CharFilter,ChoiceFilter, DateTimeFilter
from rest_framework import status

class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    status = ChoiceFilter(choices=STATUS_CHOICES)

class TaskHistoryFilter(FilterSet):
    status = ChoiceFilter(choices=STATUS_CHOICES)
    created_date= DateTimeFilter(lookup_expr="icontains")

class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "completed", "status", "priority"]

class TaskHistorySerializer(ModelSerializer):
    task = TaskSerializer(read_only=False)
    class Meta:
        model = TaskHistory
        fields = ["id", "status", "task", "created_date"]
    
class HistoryViewSet(LoginRequiredMixin, ModelViewSet):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskHistoryFilter
    def get_queryset(self):
        return TaskHistory.objects.filter(task__user=self.request.user)

    """ Dynamically create a TaskHistory with a simultaneous new Task """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.create(**serializer.data['task'], user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """   Currently Accepting no Updates  """
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

class TaskViewSet(LoginRequiredMixin, ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        return Task.objects.filter(deleted=False, user=self.request.user)

class TaskRestApiView(APIView):
    def get(self, request):
        tasks = [{'id':task.id, 'title':task.title, 'status':task.status} for task in Task.objects.filter(user = self.request.user)]
        return Response({'tasks':tasks})