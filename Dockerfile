FROM python:alpine

RUN pip install httplib2

WORKDIR /app
COPY . .

CMD ["python", "get_ab_items.py"]
