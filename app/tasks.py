from celery import shared_task

@shared_task(bind=True, acks_late=True)
def ShowMessage(self, msg1, msg2):
    print(msg1)
    print(msg2)
    print(self.request.id)
    print(self.request.eta)
    return "done"