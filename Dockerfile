FROM python:3.10-slim-buster

RUN mkdir -p /challenge
COPY challenge/* /challenge/
COPY requirements.txt /
WORKDIR /
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "challenge:application", "--host", "0.0.0.0", "--port", "8000"]