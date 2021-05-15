FROM python:3.9-slim-buster
RUN  pip3 install flask flask-wtf email_validator requests flask-login flask-sqlalchemy
COPY coffee-shops-login-registration coffee-shops-login-registration
CMD python3 coffee-shops-login-registration/app.py
#COPY flask-project flask-project
#CMD python3 flask-project/app.py
