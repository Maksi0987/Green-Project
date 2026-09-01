import os

# Настройки экспорта
IGNORE_DIRS = {'.venv', '.idea', '.git', '__pycache__', 'migrations', 'media', 'static'}
ALLOWED_EXTENSIONS = {'.py', '.html'}
OUTPUT_FILE = 'project_context.txt'


def collect_project_context(root_dir='.'):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Исключаем игнорируемые директории из обхода
            dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

            for file in filenames:
                ext = os.path.splitext(file)[1]
                if ext in ALLOWED_EXTENSIONS and file != os.path.basename(__file__):
                    filepath = os.path.join(dirpath, file)

                    # Форматируем заголовок файла для удобного чтения
                    outfile.write(f"\n{'=' * 60}\n")
                    outfile.write(f"FILE: {filepath}\n")
                    outfile.write(f"{'=' * 60}\n\n")

                    try:
                        with open(filepath, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read() + '\n')
                    except Exception as e:
                        outfile.write(f"# Ошибка чтения файла: {e}\n")


if __name__ == '__main__':
    collect_project_context()
    print(f"Экспорт завершен. Данные сохранены в {OUTPUT_FILE}")