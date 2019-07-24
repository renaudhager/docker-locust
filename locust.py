from locust import HttpLocust, TaskSet, task, events
# import resource
import os
from datadog import initialize, statsd

if os.environ['DATADOG_ENABLE'] == "true":
        initialize(statsd_host=os.environ['DATADOG_HOST'], statsd_port=8125)

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

    def __init__(self):
        super(DockerHttpLocust, self).__init__()

        if os.environ['DATADOG_ENABLE'] == "true":
            events.request_success += self.hook_request_success
            # locust.events.request_failure += self.hook_request_fail

    def hook_request_success(self, request_type, name, response_time, response_length):

        tags_response_time = []
        tags_response_time.append('path:' + name)
        tags_response_time.append('host:' + self.host)
        statsd.gauge("locust.response_time", response_time, tags_response_time)

        tags_total_requests = []
        tags_total_requests.append('success')
        tags_total_requests.append('path:' + name)
        tags_total_requests.append('host:' + self.host)
        statsd.increment("locust.response_time", tags_total_requests)

    # def hook_request_fail(self, request_type, name, response_time, exception):
    #     self.request_fail_stats.append([name, request_type, response_time, exception])
