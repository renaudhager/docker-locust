from locust import HttpLocust, TaskSet, task
import resource
import os

class DockerTaskSet(TaskSet):
    @task(1)
    def healthcheck(self):
        self.client.get(os.environ['URL_PATH'])

class DockerHttpLocust(HttpLocust):
    weight = 5
    host = os.environ['URL_HOST']
    task_set = DockerTaskSet
    min_wait = 1000
    max_wait = 2000
