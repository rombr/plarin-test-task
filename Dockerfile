FROM python:3.8-slim-buster

ADD requirements.txt /code/requirements.txt
ADD src /code/
ADD run.sh /code/

RUN pip install -r /code/requirements.txt

WORKDIR /code/
EXPOSE 8000
ENTRYPOINT ["/code/run.sh"]
