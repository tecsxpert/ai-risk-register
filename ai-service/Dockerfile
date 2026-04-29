# I'm using the official Python 3.11 slim image for a smaller footprint
FROM python:3.11-slim

WORKDIR /app

# I'm installing my dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now I'll copy the rest of my application code
COPY . .

# Expose port 5000 which is what my Flask app runs on
EXPOSE 5000

# I shouldn't run this with debug=True in Docker, so I'll just use Flask run or python app.py
CMD ["python", "app.py"]
