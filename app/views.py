from uuid import uuid3, uuid4
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import MyForms
from datetime import datetime
from django.contrib import messages

from celery.result import AsyncResult

# Celery Beat
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from django.utils.timezone import localtime, timedelta
import json
# Create your views here.

import pytz

def Home(request):
    if request.method == "POST":
        form = MyForms(request.POST)
        if form.is_valid():

            msg = request.POST.get("msg")
            # date = request.POST.get("date")
            # time = request.POST.get("time")

            date_time = request.POST.get("date_time")
            print(date_time)

            print(f"message: {msg}")

            # str_time = f"{date} {time}"
            # print(str_time)

            # started_at = datetime.strptime(str_time, "%Y-%m-%d %H:%M")
            
            started_at = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
            print(f"started at: {started_at}")

            cTZ = pytz.timezone("Asia/Bangkok")
            current_time = datetime.now(cTZ)
            print(f"current time: {current_time}")

            second = started_at - current_time.replace(tzinfo=None)
            print(f"count_second: {second.seconds}")
            count_second = second.seconds
            # ShowMessage.apply_async(("message", msg), eta=started_at)
            # task_id = ShowMessage.apply_async(("message", msg), countdown=count_second)

            taskName = f"Add Scheduler id {str(uuid4())}"
            xargs = json.dumps(["test_command", msg])
            task_id = RunScheduleTask(taskName, "app.tasks.ShowMessage", xargs, count_second )

            print(task_id)
            
            messages.info(request, task_id)

            return redirect("Home")

    forms = MyForms()
    context = {
        "title": "Task",
        "form": forms
    }
    return render(request, "index.html", context)


def get_task_status(request, task_id):
    task_result = AsyncResult(task_id)
    retsult = {
        "task_is": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
        "task_state": task_result.state
    } 
    return JsonResponse(retsult, status=200)

def HomeBeat(request):
   
    now = localtime()
    
    clocked, _ = ClockedSchedule.objects.get_or_create(
        clocked_time=now + timedelta(seconds=10)
    )

    task_name = str(uuid4())

    task = PeriodicTask.objects.create(
        clocked=clocked,
        name=task_name,
        task="app.tasks.ShowMessage",
        args=json.dumps(["command", f"task_name : {task_name}"]),
        expires=now + timedelta(seconds=15),
        one_off=True,
        
    )

    print(task)
    context = {
        "title": "Celery beat"
    }
    return render(request, 'home_beat.html', context)

def RunScheduleTask(task_name, task, xargs, timeInSecond):
   
    now = localtime()
    
    clocked, _ = ClockedSchedule.objects.get_or_create(
        clocked_time=now + timedelta(seconds=timeInSecond)
    )


    taskId = PeriodicTask.objects.create(
        clocked=clocked,
        name=task_name,
        task=task,
        args=xargs,
        expires=now + timedelta(seconds=timeInSecond + 1),
        one_off=True,
        
    )

    return taskId
