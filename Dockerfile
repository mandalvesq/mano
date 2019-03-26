FROM python:3.6-alpine

LABEL author="Amanda Quinto"

# add requirements file
COPY requirements.txt /code/requirements.txt

# install requirements
RUN pip install -r /code/requirements.txt

# Seta variaveis de ambiente
ENV LANG en_US.UTF-8

COPY *.py /code/
WORKDIR /code/
ENTRYPOINT ["python"]
CMD ["sabota.py"]
