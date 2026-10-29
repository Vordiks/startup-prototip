#!/usr/bin/env bash
# Устанавливаем библиотеки
pip install -r requirements.txt
# Собираем статику (CSS)
python manage.py collectstatic --no-input
# Применяем миграции (создаем базу)
python manage.py migrate