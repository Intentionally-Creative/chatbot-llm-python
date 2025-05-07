# --- 1. base image ---
  FROM python:3.12-slim

  # --- 2. install dependencies ---
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  
  # --- 3. copy project code ---
  COPY . .
  
  # --- 4. runtime config ---
  ENV PYTHONUNBUFFERED=1
  EXPOSE 8000
  
  # --- 5. launch ---
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  