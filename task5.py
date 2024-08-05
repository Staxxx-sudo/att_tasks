import logging
from datetime import datetime, timedelta
import calendar
import re
import argparse

# Настройка логирования
logging.basicConfig(filename='date_conversion_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Сопоставление русских и английских названий дней недели и месяцев
weekday_translation = {
    'понедельник': 'Monday',
    'вторник': 'Tuesday',
    'среда': 'Wednesday',
    'четверг': 'Thursday',
    'пятница': 'Friday',
    'суббота': 'Saturday',
    'воскресенье': 'Sunday'
}

month_translation = {
    'января': 'January',
    'февраля': 'February',
    'марта': 'March',
    'апреля': 'April',
    'мая': 'May',
    'июня': 'June',
    'июля': 'July',
    'августа': 'August',
    'сентября': 'September',
    'октября': 'October',
    'ноября': 'November',
    'декабря': 'December'
}

def convert_to_date(text):
    # Регулярное выражение для парсинга входного текста
    pattern = re.compile(r"(\d*)-?(й|я)? ?(\w+)? ?(\w+)?")
    match = pattern.match(text)
    
    # Если формат не соответствует, логируем ошибку
    if not match:
        logging.error(f"Некорректный формат: {text}")
        return None
    
    # Извлечение данных из входного текста
    week_number, week_suffix, weekday_name, month_name = match.groups()
    
    # Получение текущих значений
    current_date = datetime.now()
    current_weekday_name = current_date.strftime('%A').lower()
    current_month_name = current_date.strftime('%B').lower()
    
    # Установка значений по умолчанию
    week_number = int(week_number) if week_number else 1
    weekday_name = weekday_name if weekday_name else current_weekday_name
    month_name = month_name if month_name else current_month_name
    
    try:
        # Перевод названий на английский для работы с модулем datetime
        month_name_eng = month_translation[month_name.lower()]
        weekday_name_eng = weekday_translation[weekday_name.lower()]
        # Получение номера месяца
        month_number = list(calendar.month_name).index(month_name_eng)
        # Получение номера дня недели
        weekday_number = list(calendar.day_name).index(weekday_name_eng)
    except (ValueError, KeyError) as e:
        # Логирование ошибки при конвертации данных
        logging.error(f"Ошибка при конвертации: {text} - {e}")
        return None
    
    # Проверка корректности номера недели
    if week_number < 1 or week_number > 5:
        logging.error(f"Неверный номер недели: {week_number}")
        return None
    
    # Находим первый день месяца
    first_day_of_month = datetime(current_date.year, month_number, 1)
    first_weekday_of_month = first_day_of_month.weekday()
    
    # Рассчитываем смещение до нужного дня недели
    days_to_add = (weekday_number - first_weekday_of_month + 7) % 7
    first_occurrence = first_day_of_month + timedelta(days=days_to_add)
    
    # Находим нужный день
    target_date = first_occurrence + timedelta(weeks=week_number-1)
    
    # Проверка, что дата находится в правильном месяце
    if target_date.month != month_number:
        logging.error(f"Недопустимая дата: {text}")
        return None
    
    return target_date

def main():
    parser = argparse.ArgumentParser(description="Конвертация текстового описания даты в дату текущего года.")
    args = parser.parse_args()

    while True:
        user_input = input("Введите желаемую дату для анализа (или нажмите Enter для выхода): ").strip()
        if not user_input:
            break
        date = convert_to_date(user_input)
        if date:
            print(f"Дата для '{user_input}': {date.strftime('%Y-%m-%d')}")
        else:
            print(f"Не удалось конвертировать дату для '{user_input}'")

if __name__ == "__main__":
    main()
