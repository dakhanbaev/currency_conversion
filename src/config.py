import os


def get_postgres_uri() -> str:
    host = os.environ.get("DB_HOST", "localhost")
    port = 5432 if host == "localhost" else 5432
    password = os.environ.get("POSTGRES_PASSWORD", "abc123")
    user = os.environ.get("POSTGRES_USER", "postgres")
    db_name = os.environ.get("POSTGRES_DB", "postgres")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url() -> str:
    host = os.environ.get("API_HOST", "localhost")
    port = 8000 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_exchangerate_api_url() -> str:
    api_token = os.environ.get("API_TOKEN")
    url = "https://v6.exchangerate-api.com/v6/{}/latest/"
    return url.format(api_token)

