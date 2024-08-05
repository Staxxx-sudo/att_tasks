import os
import logging
from collections import namedtuple

# Настройка логирования
logging.basicConfig(filename='directory_contents.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Определение структуры данных
FileInfo = namedtuple('FileInfo', ['name', 'extension', 'is_directory', 'parent_directory'])

def collect_directory_info(directory_path):
    """Собирает информацию о содержимом директории."""
    if not os.path.isdir(directory_path):
        logging.error(f"Указанный путь не является директорией: {directory_path}")
        print(f"Ошибка: '{directory_path}' не является директорией.")
        return
    
    logging.info(f"Начинаем обработку директории: {directory_path}")
    
    try:
        # Проход по всем каталогам и файлам в указанной директории
        for root, dirs, files in os.walk(directory_path):
            logging.info(f"Обрабатываем каталог: {root}")
            
            for name in dirs:
                # Для каталогов
                dir_path = os.path.join(root, name)
                parent_dir = os.path.basename(root)
                file_info = FileInfo(
                    name=name,
                    extension=None,
                    is_directory=True,
                    parent_directory=parent_dir
                )
                logging.info(f"Каталог: {file_info}")
            
            for name in files:
                # Для файлов
                file_path = os.path.join(root, name)
                parent_dir = os.path.basename(root)
                name_without_ext, ext = os.path.splitext(name)
                file_info = FileInfo(
                    name=name_without_ext,
                    extension=ext[1:],  # убираем точку из расширения
                    is_directory=False,
                    parent_directory=parent_dir
                )
                logging.info(f"Файл: {file_info}")
                
    except PermissionError as e:
        logging.error(f"Ошибка доступа к директории '{directory_path}': {e}")
    except FileNotFoundError as e:
        logging.error(f"Файл или директория не найдены при обработке '{directory_path}': {e}")
    except OSError as e:
        logging.error(f"OS ошибка при обработке '{directory_path}': {e}")
    except Exception as e:
        logging.error(f"Неизвестная ошибка при сборе информации из '{directory_path}': {e}")

def main():
    while True:
        # Запрос директорий у пользователя
        directories_input = input("Введите пути до директорий, разделенные пробелом (или нажмите Enter для выхода): ")
        
        # Проверка на пустую строку
        if not directories_input.strip():
            print("Завершение программы.")
            break

        directories = directories_input.split()
        
        # Обработка каждой директории
        for directory in directories:
            if os.path.isdir(directory):
                print(f"Обрабатывается директория: {directory}")
                collect_directory_info(directory)
            else:
                # Если директория не существует, записываем ошибку в лог
                logging.error(f"Указанный путь не является директорией: {directory}")
                print(f"Ошибка: '{directory}' не является директорией.")

if __name__ == "__main__":
    main()
