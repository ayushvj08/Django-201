from rest_framework.views import APIView
from .models import Task, STATUS_CHOICES, TaskHistory
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend,FilterSet,CharFilter,ChoiceFilter, DateTimeFilter

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

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            status = TaskSerializer(data=validated_data).initial_data.get('status')
            if self.instance.status != status:
                task_history = TaskHistory(status=status, task=self.instance)
                task_history.save()

            self.instance = self.update(self.instance, validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(validated_data)
            task_history = TaskHistory(status=self.instance.status, task=self.instance)
            task_history.save()
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

class TaskHistorySerializer(ModelSerializer):
    task = TaskSerializer(read_only=True)
    class Meta:
        model = TaskHistory
        fields = ["id", "status", "task", "created_date"]
    
class HistoryViewSet(ReadOnlyModelViewSet):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskHistoryFilter
    def get_queryset(self):
        return TaskHistory.objects.filter(task__user=self.request.user)

class TaskViewSet(ModelViewSet):
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