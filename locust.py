"""
Module that run HTTP load test and send metrics to Datadog.
"""

from locust import HttpLocust, TaskSet, task, events
import os
from datadog import initialize, statsd

if os.environ['DATADOG_ENABLE'] == "true":
    initialize(statsd_host=os.environ['DATADOG_HOST'], statsd_port=8125)

class DockerTaskSet(TaskSet):
    """
    TaskSet class definition
    """
    @task(1)
    def healthcheck(self):
        self.client.get(os.environ['URL_PATH'])

class DockerHttpLocust(HttpLocust):
    """
    HttpLocust class definition.
    Main class
    """
    weight = 5
    host = os.environ['URL_HOST']
    task_set = DockerTaskSet
    min_wait = 1000
    max_wait = 2000

    def __init__(self):
        super(DockerHttpLocust, self).__init__()

        if os.environ['DATADOG_ENABLE'] == "true":
            events.request_success += self.hook_request_success
            events.request_failure += self.hook_request_fail

    def hook_request_success(self, request_type, name, response_time, response_length):
        """
        Function to send metrics to Datadog when a request is successful
        """
        tags_response_time = []
        tags_response_time.append('staus:success')
        tags_response_time.append('path:' + name)
        tags_response_time.append('host:' + self.host)

        statsd.histogram("locust.response_time", response_time, tags=tags_response_time)

        tags_total_requests = []
        tags_total_requests.append('staus:success')
        tags_total_requests.append('path:' + name)
        tags_total_requests.append('host:' + self.host)

        statsd.increment("locust.total_requests", tags=tags_total_requests)

    def hook_request_fail(self, request_type, name, response_time, exception):
        """
        Function to send metrics to Datadog when a request is failed
        """
        tags_response_time = []
        tags_response_time.append('status:fail')
        tags_response_time.append('path:' + name)
        tags_response_time.append('host:' + self.host)
        statsd.gauge("locust.response_time", response_time, tags=tags_response_time)

        tags_total_requests = []
        tags_total_requests.append('status:fail')
        tags_total_requests.append('path:' + name)
        tags_total_requests.append('host:' + self.host)
        statsd.increment("locust.total_requests", tags=tags_total_requests)
