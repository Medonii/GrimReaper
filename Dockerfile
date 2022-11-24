FROM python:3.11

# 
WORKDIR /GrimReaper

# 
COPY requirements.txt requirements.txt

# 
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# 
COPY user /GrimReaper/user/ 

ENV PYTHONPATH "${PYTHONPATH}:/GrimReaper/user/"

# 
CMD ["uvicorn", "user.index:app", "--host", "0.0.0.0", "--port", "80"]