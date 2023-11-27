FROM python
RUN pip install --upgrade pip wheel uwsgi bottle
WORKDIR /app
COPY app.py uwsgi.sh /app/
CMD ["bash", "uwsgi.sh"]
