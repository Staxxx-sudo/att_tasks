import os
import logging
import time

# Настройка логирования
logging.basicConfig(filename='rename_files.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def rename_files(folder, desired_name, num_digits, source_ext, target_ext, name_range):
    try:
        if not os.path.exists(folder):
            raise FileNotFoundError(f"Директория не существует: {folder}")

        files = [f for f in os.listdir(folder) if f.endswith(f'.{source_ext}')]
        if not files:
            raise FileNotFoundError(f"Нет файлов с расширением {source_ext} в директории {folder}")
        
        files.sort()
        success = False

        for i, file_name in enumerate(files, start=1):
            try:
                file_number = str(i).zfill(num_digits)

                # Проверка допустимости диапазона
                if name_range[1] > len(file_name) or name_range[0] > len(file_name):
                    raise ValueError(f"Диапазон {name_range} выходит за пределы длины имени файла: {file_name}")

                original_name_part = file_name[name_range[0]-1:name_range[1]]
                new_file_name = f"{original_name_part}{desired_name}{file_number}.{target_ext}"
                new_path = os.path.join(folder, new_file_name)

                # Проверка существования файла с целевым именем
                if os.path.exists(new_path):
                    raise FileExistsError(f"Файл с именем {new_file_name} уже существует. Пропуск переименования.")

                original_path = os.path.join(folder, file_name)
                os.rename(original_path, new_path)

                success = True
                message = f"Файл {file_name} переименован в {new_file_name}"
                logging.info(message)
                print(message)

            except Exception as e:
                message = f"Ошибка при переименовании файла {file_name}: {e}"
                logging.error(message)
                print(message)

        if success:
            message = f"Успешное переименование файлов в директории {folder}"
        else:
            message = f"Не удалось переименовать файлы в директории {folder}"

        logging.info(message)
        print(message)

    except Exception as e:
        message = f"Ошибка в функции rename_files: {e}"
        logging.error(message)
        print(message)
        raise

def main():
    directories = []
    total_inputs = 0

    while True:
        start_time = time.time()
        try:
            folder = input("Введите путь к директории: ")
            if folder.lower() == 'stop':
                logging.info(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                print(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                break

            directories.append(folder)
            total_inputs += 1

            if not os.path.exists(folder):
                raise FileNotFoundError(f"Директория не существует: {folder}")

            desired_name = input("Введите желаемое конечное имя файлов: ")
            if desired_name.lower() == 'stop':
                logging.info(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                print(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                break

            if not desired_name.strip():
                raise ValueError("Желаемое имя файлов не может быть пустым.")

            try:
                num_digits = int(input("Введите количество цифр в порядковом номере: "))
            except ValueError as ve:
                raise ValueError(f"Некорректный ввод данных для количества цифр: {ve}")

            source_ext = input("Введите расширение исходного файла: ")
            if source_ext.lower() == 'stop':
                logging.info(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                print(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                break

            target_ext = input("Введите расширение конечного файла: ")
            if target_ext.lower() == 'stop':
                logging.info(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                print(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                break

            name_range = input("Введите диапазон сохраняемого оригинального имени (например, 3-6): ").split('-')
            if name_range[0].lower() == 'stop' or name_range[1].lower() == 'stop':
                logging.info(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                print(f"Программа завершена пользователем. Введено {total_inputs} примеров.")
                break

            name_range = [int(name_range[0]), int(name_range[1])]

            # Проверка на правильность введенного диапазона
            if name_range[0] > name_range[1]:
                raise ValueError(f"Начало диапазона ({name_range[0]}) не может быть больше конца диапазона ({name_range[1]})")

            logging.info(f"Запуск функции rename_files с параметрами: {desired_name}, {num_digits}, {source_ext}, {target_ext}, {name_range}, {folder}")
            rename_files(folder, desired_name, num_digits, source_ext, target_ext, name_range)

        except FileNotFoundError as fnfe:
            message = f"Произошла ошибка: {fnfe}. Пожалуйста, попробуйте снова."
            logging.error(message)
            print(message)
            continue  # Вернуться к началу цикла и запросить ввод снова

        except ValueError as ve:
            message = f"Произошла ошибка: {ve}. Некорректный ввод данных. Пожалуйста, попробуйте снова."
            logging.error(message)
            print(message)
            continue  # Вернуться к началу цикла и запросить ввод снова

        except Exception as e:
            message = f"Произошла ошибка: {e}. Пожалуйста, попробуйте снова."
            logging.error(message)
            print(message)
            continue  # Вернуться к началу цикла и запросить ввод снова

        finally:
            end_time = time.time()
            duration = end_time - start_time
            logging.info(f"Время, затраченное на ввод примера: {duration:.2f} секунд.")
            print(f"Время, затраченное на ввод примера: {duration:.2f} секунд.")

    logging.info(f"Пользователь ввел {total_inputs} примеров.")
    print(f"Пользователь ввел {total_inputs} примеров.")

if __name__ == "__main__":
    main()
