# Celery Task
## start beat
```
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
```
celery -A core beat -l info -S django
```
- add config in project setting
```
CELERYBEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
```