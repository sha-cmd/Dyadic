FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3-pip python3.10-venv
EXPOSE 80
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH
COPY . /usr/ML/app
WORKDIR /usr/ML/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python app.py
