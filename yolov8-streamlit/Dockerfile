FROM python:3.10.6-buster
WORKDIR /app
COPY packages.txt .
RUN apt-get update && \
    xargs -a packages.txt apt-get install -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* || true

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
#EXPOSE 8501
#CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
#CMD ["streamlit", "run", "app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
