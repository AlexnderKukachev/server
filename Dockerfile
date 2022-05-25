FROM python:3.9

WORKDIR /async_server

COPY . /async_server

EXPOSE 5000

CMD [ "python", "main.py"]

ADD . /requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt