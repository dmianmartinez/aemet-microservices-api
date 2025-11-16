FROM python:latest
COPY get_municipio.py datos_municipio.json requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./get_municipio.py" ]