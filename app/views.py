from django.shortcuts import redirect, render
from .forms import MyForms
from .tasks import ShowMessage

import datetime
import pytz

# Create your views here.


def Home(request):
    if request.method == "POST":
        form = MyForms(request.POST)
        if form.is_valid():

            msg = request.POST.get("msg")
            date = request.POST.get("date")
            time = request.POST.get("time")

            print(f"message: {msg}")
            # print(f"date: {date}")
            # print(f"time: {time}")

            cTz = pytz.timezone("Asia/Bangkok")

            str_time = f"{date} {time}"
            print(str_time)

            # started_at = datetime.datetime(2022, 6, 12, 22, 16, 0, tzinfo=cTz)
            started_at = datetime.datetime.strptime(
                str_time, "%Y-%m-%d %H:%M").replace(tzinfo=cTz)
            print(f"started at: {started_at}")

            current_time = datetime.datetime.now(cTz)
            print(f"current time: {current_time}")

            second = datetime.datetime.now().replace(tzinfo=cTz).second - started_at.second
            print(second)

            # ShowMessage.apply_async(("message", msg), eta=started_at)
            ShowMessage.apply_async(("message", msg), countdown=second)

            return redirect("Home")

    forms = MyForms()
    context = {
        "title": "Task",
        "form": forms
    }
    return render(request, "index.html", context)
