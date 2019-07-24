FROM python:3.5-slim

ENV CLIENTS=100 \
  DATADOG_ENABLE=false \
  HATCHING_RATE=10 \
  OPTIONS="--no-web --print-stats"

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

WORKDIR /locust

COPY locust.py .

CMD ["sh", "-c", "locust -c $CLIENTS -r $HATCHING_RATE $OPTIONS -f locust.py DockerHttpLocust"]
