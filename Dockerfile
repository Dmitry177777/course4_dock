FROM python:3

WORKDIR /code

COPY ./requirements.txt /code/

#RUN pip install -r requirements.txt
#RUN pip install postgres
#RUN pip install redis

COPY . .

CMD python manage.py runserver