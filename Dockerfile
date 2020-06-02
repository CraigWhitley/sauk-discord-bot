FROM python:3.8

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY . /
WORKDIR /

ENV PYTHONPATH=/

CMD ["python", "app.py"]