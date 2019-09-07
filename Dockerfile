# Build base image
FROM jfloff/alpine-python:3.6


WORKDIR /finception
RUN echo $(ls -1 .)
COPY requirements.txt /finception
# Install all necessary packages
RUN pip install -r requirements.txt
COPY . /finception
EXPOSE 8000
RUN celery -A finception beat -l info &
RUN celery -A finception worker -c4 -l info &
RUN python manage.py makemigrations && python manage.py migrate
CMD ["./run.sh"]

