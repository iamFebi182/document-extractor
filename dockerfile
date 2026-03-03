FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y libmagic1 tesseract-ocr tesseract-ocr-ind && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    flask==3.0.0 \
    unstructured==0.11.0 \
    "unstructured[pdf]==0.11.0" \
    "unstructured[docx]==0.11.0" \
    "unstructured[pptx]==0.11.0" \
    python-magic-bin \
    pillow \
    pytesseract

WORKDIR /app
COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
