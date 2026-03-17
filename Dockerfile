FROM python:3.9-slim

WORKDIR /app

#--------Install dependencies in requirements.txt file--------
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

#-------Copy the application and data-----------------
COPY main.py .
COPY movies.csv .

#---------Expose the port FastAPI runs on----------------
EXPOSE 80

#------------Command to run the application--------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]