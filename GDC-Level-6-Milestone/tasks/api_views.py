from django.views import View
from django.http.response import JsonResponse
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from tasks.models import Task

from rest_framework.viewsets import ModelViewSet


class TaskRestApiView(APIView):
    def get(self, request):
        task_titles = [task.title for task in Task.objects.all()]
        return Response(task_titles)

class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = ["title", "completed"]

class ApiView(ModelViewSet):
    queryset = Task.objects.all()
    tasks = Task.objects.all()
    data = TaskSerializer(tasks, many=True).data
    # return Response({"tasks": data})     
    # def get(self, request):
        # queryset = Task.objects.all()
        # tasks = Task.objects.all()
        # data = TaskSerializer(tasks, many=True).data
        # return Response({"tasks": data})            
        # tasks = Task.objects.all()
        # data = []
        # for task in tasks:
        #     data.append({"id": task.id, "title": task.title, "priority": task.priority, "description": task.description})
        # return Response({"tasks": data})