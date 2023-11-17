FROM python:3.10-bullseye

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /source
WORKDIR /source

CMD ["python", "wsgi.py"]