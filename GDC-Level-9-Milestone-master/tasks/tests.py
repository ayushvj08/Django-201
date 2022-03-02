from django.test import TestCase, RequestFactory
from .tasks import send_email_reminder
from .models import User, Task
from .views import TaskListView, TaskCreateView, DeleteTaskView

class QuestionModelTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="bruce_wayne", email="bruce@wayne.org", password="i_am_batman")
        self.task = Task.objects.create(title="Hello World", description="My new Task", priority=1)

    def test_unauthorised(self):
        """
        Try to GET the tasks listing page, expect the response to redirect to the login page
        """
        response = self.client.get("/task/list/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user/login/?next=/task/list/")


    def test_authenticated(self):
        """
        Try to GET the tasks listing page, expect the response to redirect to the login page
        """
        # Create an instance of a GET request.
        request = self.factory.get("/task/list/")
        # Set the user instance on the request.
        request.user = self.user
        # We simply create the view and call it like a regular function
        response = TaskListView.as_view()(request)
        # Since we are authenticated we get a 200 response
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        # request = self.factory.get("/task/new/")
        # request.user = self.user
        request = self.factory.post("/task/new/", {'title':'Task', 'description':'some description for task', 'priority':1})
        request.user = self.user
        response = TaskCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
