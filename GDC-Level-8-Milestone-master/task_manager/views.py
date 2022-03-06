from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "p-label rounded"
        self.fields['password1'].widget.attrs['class'] = "p-label rounded"
        self.fields['password2'].widget.attrs['class'] = "p-label rounded"

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "p-label rounded"
        self.fields['password'].widget.attrs['class'] = "p-label rounded"

class UserCreateView(CreateView):
    form_class = UserForm
    template_name = "user_create.html"
    success_url = "/user/login/"

class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = "user_login.html"