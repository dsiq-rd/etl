import os	
from celery import Celery, chain, group, beat, task
from config import environment_type as env

environment = env["development"]

app = Celery('tasks',
	broker=environment.get('broker'),
	backend=environment.get('backend')
	)
