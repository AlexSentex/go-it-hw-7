from pathlib import Path
import sys
import shutil
import re

extensions = {
    '.jpg': 'pictures',
    '.jpeg': 'pictures',
    '.png': 'pictures',
    '.bmp': 'pictures',
    '.svg': 'pictures',
    '.mkv': 'videos',
    '.avi': 'videos',
    '.mp4': 'videos',
    '.mov': 'videos',
    '.doc': 'documents',
    '.docx': 'documents',
    '.txt': 'documents',
    '.pdf': 'documents',
    '.xlsx': 'documents',
    '.pptx': 'documents',
    '.mp3': 'music',
    '.ogg': 'music',
    '.wav': 'music',
    '.amr': 'music',
    '.zip': 'archives',
    '.tar': 'archives',
    '.gz': 'archives'
}

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
ENG_SYMBOLS = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANSLATION = {}
for c, l in zip(CYRILLIC_SYMBOLS, ENG_SYMBOLS):
    TRANSLATION[ord(c)] = l
    TRANSLATION[ord(c.upper())] = l.upper()

PICTURES = []
MUSIC = []
VIDEOS = []
DOCUMENTS = []
ARCHIVES = []
OTHER = []

RECOGN_EXT = set()
UNRECOGN_EXT = set()


def sanitize_folder(src: Path, outp: Path) -> None:
    for item in src.iterdir(): # ітеруємось по папці
        if item.is_dir():       # перевіряємо чи це папка
            if item.name in (           # пропускаємо папки у які переміщуємо
                            'pictures',
                            'videos',
                            'documents',
                            'music',
                            'archives',
                            'Other'
                            ):
                continue
            sanitize_folder(item, outp) # рекурсія
        else:
            move_file(item, outp, src) # переміщуємо файл
    for folder in src.iterdir():
        if folder.is_dir() and folder.name not in (           # пропускаємо папки у які перемістили
                            'pictures',
                            'videos',
                            'documents',
                            'music',
                            'archives',
                            'Other'
                            ):
           folder.rmdir() # видаляємо пусті папки


def move_file(file: Path, TARGET, LOCATION) -> None:
    ext = file.suffix[1:]       # беремо розширення файлу для списку знайдених розширень
    name = file.name[:-len(file.suffix)]        # беремо ім'я файлу без розширення

    if file.suffix in extensions:       # перевіряємо чи файл є у відомих розширеннях
        
        # створюємо папку якщо немає такої
        folder = extensions[file.suffix]
        Path.mkdir(Path.joinpath(TARGET, folder), exist_ok=True, parents=True)

        """ 
        Додаємо назву файлу у список файлів відповідної категорії

        P.S. Не знаю чи взагалі часто цим користуються, з одної сторони зручно, 
             а з другої, цікаво почути коментар з цього приводу
        """
        globals()[folder.upper()].append(normalize(name) + file.suffix)
        
        if file.suffix in ['.zip', '.tar', '.gz']:
            # розпаковуємо архіви
            shutil.unpack_archive(file, Path.joinpath(TARGET, folder, normalize(name)))
            file.unlink()
            return
        else:
            # присвоюємо шлях для переміщення файлів
            path = Path.joinpath(LOCATION, folder, normalize(name) + file.suffix)

        # додаємо у сет знайдених відомих розширень
        RECOGN_EXT.add(ext)

    else:
        Path.mkdir(Path.joinpath(TARGET, 'Other'), exist_ok=True, parents=True)
        path = Path.joinpath(LOCATION, 'Other', normalize(name) + file.suffix)

        # додаємо у сет знайдених невідомих розширень
        UNRECOGN_EXT.add(ext)

        # Додаємо назву файлу у список файлів відповідної категорії
        OTHER.append(normalize(name) + file.suffix)

    shutil.move(file, path)

def normalize(name: str) -> str:        # нормалізуємо назви
    name = name.translate(TRANSLATION)
    name = re.sub(r'\W', '_', name)
    return name

def main():
    LOCATION = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    TARGET = Path(sys.argv[2] if len(sys.argv) > 2 else LOCATION)
    sanitize_folder(LOCATION, TARGET)
    print('Recognized extensions: {}'.format(re.sub(r'{|}|\'|"', '', RECOGN_EXT.__str__())))
    print('Unrecognized extensions: {}'.format(re.sub(r'{|}|\'|"', '', UNRECOGN_EXT.__str__())))
    print('Pictures: {}'.format(re.sub(r'{|}|\'|"|\[|\]', '', PICTURES.__str__())))
    print('Music: {}'.format(re.sub(r'{|}|\'|"|\[|\]', '', MUSIC.__str__())))
    print('Videos: {}'.format(re.sub(r'{|}|\'|"|\[|\]', '', VIDEOS.__str__())))
    print('Documents: {}'.format(re.sub(r'{|}|\'|"|\[|\]', '', DOCUMENTS.__str__())))
    print('Archives: {}'.format(re.sub(r'{|}|\'|"|\[|\]', '', ARCHIVES.__str__())))
    print('Other: {}'.format(re.sub(r'{|}|\'|"|\[|\]', '', OTHER.__str__())))

if __name__ == "__main__":
    main()
    