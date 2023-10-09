FROM python:3.10-bullseye

EXPOSE 8000
COPY src /home/app/src
WORKDIR /home/app/src
CMD ["python", "-m", "http.server"]
