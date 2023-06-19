FROM python
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY ./app /app
WORKDIR /app
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
