FROM python:3.8.1

RUN mkdir -p /ws
RUN mkdir -p /data
VOLUME /data
WORKDIR /ws
COPY requirements.txt  /ws/requirements.txt
RUN pip install -r requirements.txt
COPY . /ws/

CMD python run.py


