FROM python:latest
COPY get_demo_municipio.py datos_municipio.json requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./get_demo_municipio.py" ]