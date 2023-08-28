FROM python:3.10 as builder

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

FROM python:3.10-slim

WORKDIR ./app
EXPOSE 8501

COPY --from=builder /wheels /wheels

RUN pip install --no-cache /wheels/* && mkdir ./.streamlit

COPY ./app .
COPY .streamlit ./.streamlit

ENTRYPOINT ["streamlit", "run", "⭐️_Home.py", "--server.port=8501", "--server.address=172.17.0.2"]
