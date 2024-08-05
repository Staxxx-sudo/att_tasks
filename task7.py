import os
import logging
import time
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='file_info.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Настройка логирования пользовательских действий
user_log = logging.getLogger('user_log')
user_log.setLevel(logging.DEBUG)
fh = logging.FileHandler('user_activity.log')
formatter = logging.Formatter('%(asctime)s:%(message)s')
fh.setFormatter(formatter)
user_log.addHandler(fh)

def get_file_info(file_path):
    """Получает информацию о файле: путь, имя и расширение."""
    try:
        # Проверка существования пути
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Путь не существует: {file_path}")
        
        # Получаем имя файла с расширением
        file_name_with_ext = os.path.basename(file_path)
        
        # Разделяем имя файла на имя и расширение
        file_name, file_extension = os.path.splitext(file_name_with_ext)
        
        # Получаем путь к директории
        directory_path = os.path.dirname(file_path)
        
        # Логируем успешную обработку
        logging.info(f"Успешно обработан файл: {file_path}")
        
        # Возвращаем кортеж с результатами
        return (directory_path, file_name, file_extension)
    
    except Exception as e:
        logging.error(f"Ошибка при обработке пути '{file_path}': {e}")
        return (None, None, None)

def main():
    file_paths = []
    start_time = time.time()
    user_log.info("Начало работы программы")
    
    while True:
        path = input("Введите путь к файлу (или 'stop' для завершения ввода): ")
        user_log.info(f"Ввод пользователя: {path}")
        
        if path.lower() == 'stop':
            break
        
        file_paths.append(path)
    
    total_files = len(file_paths)
    user_log.info(f"Количество введенных путей: {total_files}")

    for path in file_paths:
        start_request_time = time.time()
        print(f"Обрабатывается путь: {path}")
        file_info = get_file_info(path)
        end_request_time = time.time()
        
        if file_info[0] is not None:
            print(f"Путь: {file_info[0]}")
            print(f"Имя файла: {file_info[1]}")
            print(f"Расширение: {file_info[2]}")
        else:
            print(f"Не удалось получить информацию о файле: {path}")
        
        user_log.info(f"Ответ программы для {path}: {file_info}")
        user_log.info(f"Время обработки запроса: {end_request_time - start_request_time:.2f} секунд")
    
    end_time = time.time()
    total_time = end_time - start_time
    user_log.info(f"Общее время работы программы: {total_time:.2f} секунд")
    print(f"Общее количество введенных путей: {total_files}")
    print(f"Общее время работы программы: {total_time:.2f} секунд")

if __name__ == "__main__":
    main()
