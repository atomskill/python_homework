FROM python:3.10-bullseye

RUN pip install flask

COPY src /home/flask/src
ENV port=15155
WORKDIR /home/flask/src
CMD ["python", "app.py"]
