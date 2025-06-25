FROM python:3.13

LABEL "maintainer"="Sunil Chelaramani"

COPY app /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD ["uvicorn", "context.main:app", "--host", "0.0.0.0", "--port", "8000"]