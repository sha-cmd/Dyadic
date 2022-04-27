FROM continuumio/anaconda3:5.3.0
COPY . /usr/ML/app
EXPOSE 80
WORKDIR /usr/ML/app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python app.py
