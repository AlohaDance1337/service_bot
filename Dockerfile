FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /service_bot

# Копируем файлы pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock ./

# Устанавливаем curl и poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Блокируем зависимости
RUN poetry lock

# Устанавливаем зависимости в виртуальное окружение
RUN poetry install --no-root --only main

# Копируем остальной код проекта
COPY . .

# Запускаем приложение через poetry
CMD ["poetry", "run", "python", "service_bot/main.py"]

