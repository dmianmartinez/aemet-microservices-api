FROM python:latest
COPY get_meteo_municipio.py requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "./get_meteo_municipio.py" ]