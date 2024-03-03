from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from .custom_decorator import anonymous_required

app_name = "ProcomChatbot_App"


urlpatterns = [
    # Primary Views
    path("", login_required(views.chatbot), name="chatbot"),
    path("error_page/", login_required(views.error_page), name="error_page"),
    # Account Related Views
    path("login/", anonymous_required(views.user_login), name="user_login"),
    path("logout/", login_required(views.user_logout), name="user_logout"),
    path("register/", anonymous_required(views.user_register), name="user_register"),
    # API
    path("api/send-message/", login_required(views.send_message), name="send_message"),
]
