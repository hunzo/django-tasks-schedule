from django.urls import path
from .views import Home, get_task_status, HomeBeat

urlpatterns = [
    path("", Home, name="Home"),
    path("beat/", HomeBeat, name="beat"),
    path("task/<task_id>", get_task_status, name="task_status" ),

]