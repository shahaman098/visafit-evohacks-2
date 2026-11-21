# Reproducible VisaFit demo for judges
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY visafit ./visafit
COPY README.md THEME.md SUBMISSION.md ./
EXPOSE 8791
CMD ["uvicorn", "visafit.app:app", "--host", "0.0.0.0", "--port", "8791"]
