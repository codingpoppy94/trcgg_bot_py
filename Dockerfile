FROM python:3.10.0

COPY ./src /src
COPY requirements.txt /src

WORKDIR /src

RUN pip install -r requirements.txt

# CMD ["uvicorn", "main:app"]
# CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "80"]
# CMD ["fastapi", "run", "src/main.py", "--port", "80"]

EXPOSE 24001
CMD ["python", "main.py"]