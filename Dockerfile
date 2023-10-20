FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src .
RUN mkdir exchange_history_files
CMD ["python3", "run.py"]