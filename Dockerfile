FROM python:3.4-alpine
ADD . /api
WORKDIR /api
RUN pip install -r requirements.txt
CMD ["python", "main.py"]