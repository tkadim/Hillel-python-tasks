#!/bin/sh

set -e

echo "======================================"
echo "Запуск entrypoint-скрипта..."
echo "======================================"

# ------------------------------------------------
# 1. ОЧІКУВАННЯ ГОТОВНОСТІ POSTGRESQL
# ------------------------------------------------

if [ "$POSTGRES_HOST" ]; then
    echo "\n -Очікування доступності PostgreSQL на $POSTGRES_HOST:$POSTGRES_PORT..."

    # nc (netcat) перевіряє, чи порт бази реально приймає з'єднання
    while ! nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}"; do
        echo "PostgreSQL ще не готовий - чекаємо 1 секунду..."
        sleep 1
    done

    echo "\n -PostgreSQL готовий до з'єднань."
else
    echo "\n -POSTGRES_HOST не встановлено - пропускаємо перевірку (ймовірно, SQLite)."
fi

# ------------------------------------------------
# 2. ЗАСТОСУВАННЯ МІГРАЦІЙ
# ------------------------------------------------
echo "\n -Застосування міграцій..."
python manage.py migrate --noinput


## ------------------------------------------------
## 3. ЗАВАНТАЖЕННЯ ДАННИХ З SQLITE БАЗИ(datadump.json) ЯКЩО POSTGRES БАЗА ПОРОЖНЯ
## ------------------------------------------------
#echo "\n -Первірка чи база postgres порожня ..."
#
#if [ -f "datadump.json" ]; then
#    echo "Знайдено файл datadump.json - завантажуємо дані..."
#    python manage.py loaddata datadump.json
#else
#    echo "Файл datadump.json не знайдено"
#fi

# ------------------------------------------------
# 3. ЗБІР СТАТИЧНИХ ФАЙЛІВ
# ------------------------------------------------
# --noinput пропускає інтерактивні питання (типу "перезаписати файли?")
echo "\n -Збір статичних файлів..."
python manage.py collectstatic --noinput

# ------------------------------------------------
# 4. (ОПЦІЙНО) АВТОМАТИЧНЕ СТВОРЕННЯ SUPERUSER ПРИ ПЕРШОМУ ЗАПУСКУ
# ------------------------------------------------

if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "\n -Перевірка/створення суперкористувача..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD',
    )
    print('\n -Суперкористувача створено.')
else:
    print('\n -Суперкористувач уже існує - пропускаємо.')
"
fi

echo "======================================"
echo "Entrypoint завершено. Запуск основної команди..."
echo "======================================"

# ------------------------------------------------
# 5. ЗАПУСК ОСНОВНОЇ КОМАНДИ
# ------------------------------------------------

exec "$@"