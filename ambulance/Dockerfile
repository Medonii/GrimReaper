FROM python:3.11

# 
WORKDIR /ambulance

# 
COPY requirements.txt requirements.txt

# 
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# 
COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/GrimReaper/ambulance/"

# 
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]