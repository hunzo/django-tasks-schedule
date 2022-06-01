from celery import shared_task
from django.contrib import messages

@shared_task(bind=True, acks_late=True)
def ShowMessage(self, msg1, msg2):
    print(msg1)
    print(msg2)
    print(self.request)
    # messages.info(self.request, msg2)
    return "done"