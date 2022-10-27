import os
from collections.abc import Iterable


def gen_files_dir(path: str, depth=1) -> Iterable[str]:
    """Рекурсивно перебираем файлы и каталоги до определенной глубины"""
    depth -= 1
    with os.scandir(path) as p:
        for entry in p:
            yield entry.path
            if entry.is_dir() and depth > 0:
                yield from gen_files_dir(entry.path, depth)


if __name__ == '__main__':
    directory = os.getcwd()
    files = list(gen_files_dir(directory))
    line_count = 0
    for file_dir in files:
        if not os.path.isfile(file_dir):
            continue

        # Откидываем файлы без расширения .py
        skip_File = True
        for ending in '.py':
            if file_dir.endswith(ending):
                skip_File = False

        if not skip_File:
            try:
                file = open(file_dir, "r")
                local_count = 0
                for line in file:
                    if line != "\n" or not line.startswith('"') or not line.startswith(
                            "#"):  # Откидываем пустые строки и комментарии <--- ТУТ НЕ РАБОТАЕТ
                        local_count += 1
                line_count += local_count

                file.close()
            except:
                continue

    print("Всего строк  - ", line_count)
