FROM python
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN apt-get install -y git
RUN git clone https://github.com/omichalo121/poldle.git
WORKDIR /poldle/app
ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
