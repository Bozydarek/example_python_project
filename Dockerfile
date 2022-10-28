FROM python:3.10

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r /code/requirements.txt

WORKDIR /code