FROM python:3.12-slim AS builder

# uvツールのインストール
COPY --from=ghcr.io/astral-sh/uv:0.7.12 /uv /uvx /bin/

WORKDIR /app

# 依存関係ファイルとREADMEをコピー
COPY pyproject.toml ./
COPY uv.lock ./

RUN uv pip install --system -r pyproject.toml

FROM python:3.12-slim AS runner

WORKDIR /app

# 依存関係と実行可能ファイルをコピー
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# アプリケーションコードをコピー
COPY src/ /app/src/
COPY .env /app/.env
COPY credentials.json /app/credentials.json

RUN useradd -m appuser
USER appuser

# 環境変数の設定
ENV PYTHONPATH=/app

CMD ["/usr/local/bin/python3", "src/main.py"]