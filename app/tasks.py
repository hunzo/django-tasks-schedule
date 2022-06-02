from celery import shared_task

@shared_task(bind=True, acks_late=True)
def ShowMessage(self, cmd, msg):

    context = {
        "cmd": cmd,
        "message": msg,
        "id": self.request.id,
        "eta": self.request.eta
    }

    print(context)
    return "done"