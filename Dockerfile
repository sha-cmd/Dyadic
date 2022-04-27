FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3-pip
RUN pip install --upgrade pip
EXPOSE 80
COPY . /usr/ML/app
WORKDIR /usr/ML/app
RUN pip install -r requirements.txt
CMD python app.py
