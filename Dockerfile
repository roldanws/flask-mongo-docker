FROM python:3.9
COPY . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 5000
CMD ["python","app.py"]