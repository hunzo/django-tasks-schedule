from django.shortcuts import redirect, render
from .forms import MyForms
from .tasks import ShowMessage
from datetime import datetime
from pprint import pprint

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
            ShowMessage.apply_async(("message", msg), countdown=count_second)


            return redirect("Home")

    forms = MyForms()
    context = {
        "title": "Task",
        "form": forms
    }
    return render(request, "index.html", context)
