FROM python:3.8.6-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
