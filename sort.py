import sys
from pathlib import Path
import shutil
import re
import os

images = []
documents = []
audio = []
video = []
archives = []
unknown = []
my_others = []
REGISTER_EXTENSION = {
    'JPEG': images,
    'JPG': images,
    'PNG': images,
    'SVG': images,
    'AVI': video, 
    'MP4': video, 
    'MOV': video, 
    'MKV': video,
    'DOC': documents, 
    'DOCX': documents,
    'TXT': documents, 
    'PDF': documents, 
    'XLSX': documents, 
    'PPTX': documents,
    'MP3': audio,
    'OGG': audio, 
    'WAV': audio, 
    'AMR': audio,
    'M4A': audio,
    'ZIP': archives,
    'GZ': archives, 
    'TAR': archives
}

DYRECTORY_NAME = {
    'JPEG': "Images",
    'JPG': "Images",
    'PNG': "Images",
    'SVG': "Images",
    'AVI': "Video", 
    'MP4': "Video", 
    'MOV': "Video", 
    'MKV': "Video",
    'DOC': "Documents", 
    'DOCX': "Documents",
    'TXT': "Documents", 
    'PDF': "Documents", 
    'XLSX': "Documents", 
    'PPTX': "Documents",
    'MP3': "Audio",
    'OGG': "Audio", 
    'WAV': "Audio", 
    'AMR': "Audio",
    'M4A': "Audio",
    'ZIP': "Archives",
    'GZ': "Archives", 
    'TAR': "Archives"
}
EXTENSION = set()

def read_folder(path: Path, folder_to_scan: Path) -> None:
    """
    Функція виконує ітераційне зчитування заданої директорії (path), відправляючи на обробку файли з цієї і вкладених директорій.

    Параметри path і folder_for_scan обов'язкові, передбачають тип даних Path.
    """
    for el in path.iterdir():
        if Path(el).is_dir():
            if el.name not in ('Archives', 'Video', 'Audio', 'Documents', 'Images', 'My others'):
                read_folder(Path(el), folder_to_scan)
        else:
            fullname = path / el.name
            handle_file(fullname, path, folder_to_scan)

def handle_file(file: Path, path: Path, folder_to_scan: Path):
    """
    Функція опрацьовує заданий файл (file) (приведення його назви у нормалізований вигляд і підбір відповідної папки для його переміщення).

    Параметри file. path і folder_to_scan обов'язкові, передбачають тип даних Path.
    """
    file_name = file.name.split('.')[0]
    ext = file.suffix[1:]
    # ext_upper = file.suffix[1:].upper()
      
    if not ext:  
        my_others.append(file.name)
        target_directory = folder_to_scan / 'My others'
        handle_folder(file, folder_to_scan, target_directory)
    else:
        # name = normalize(file_name)+ '.' + ext
        name = file_name+ '.' + ext
        file = path / name
        try:
            container = REGISTER_EXTENSION[ext.upper()]
            EXTENSION.add(ext.upper())
            container.append(file.name)
            target_directory = folder_to_scan / DYRECTORY_NAME[ext.upper()]
            handle_folder(file, folder_to_scan, target_directory)
        except KeyError:
            unknown.append(ext)
            my_others.append(file.name)
            target_directory = folder_to_scan / 'My others'
            handle_folder(file, folder_to_scan, target_directory)

def normalize(element: str) -> str:
    """
    Функція в рядку element здійснює транслітерацію кирилиці на латинський алфавіт, а також Замінює всі символи, окрім латинських літер, цифр на '_'.

    Параметр element обов'язковий, передбачає тип даних String.
    """
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    element_trans = element.translate(TRANS)
    element_trans = re.sub(r'\W^\.', '_', element_trans)    
    return element_trans

def handle_folder(file: Path, folder_to_scan: Path, target_folder: Path) -> None:
    """
    Функція створює задану папку (target_folder) і переносить в неї заданий файл (file).

    Параметрм file, folder_to_scan і target_folder - обов'язкові, передбачають тип даних Path.
    """
    target_folder.mkdir(exist_ok=True, parents=True)
    file.replace(target_folder / normalize(file.name))
    
def handle_archive(file: Path) -> None:
    """
    Функція створює папку і розпаковує в неї архів (filename).

    Параметр file обов'язковий, передбачає тип даних Path.
    """
    archive_dir = Path('Archive')
    archive_dir.mkdir(exist_ok=True, parents=True) 
    folder_for_file = archive_dir / normalize(file.name.replace(file.suffix,''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    print(f'folder_for_file = {folder_for_file}')
    archives.append(file.name)
    try:
        shutil.unpack_archive(file, folder_for_file)

    except shutil.ReadError:
        print('It is not archive')
        folder_for_file.rmdir()
    file.unlink()

def handle_empty_folders(path: Path) -> None:
    """
    Функція видаляє пусті папки із заданої директорії (path).
    
    Параметр path обов'язковий, передбачає тип даних Path.
    """
    for el in path.iterdir():
         if el.is_dir() and el.name not in ('Archives', 'Video', 'Audio', 'Documents', 'Images', 'My others'):
            try:
                el.rmdir()
            except:
                print('The folder is not emty')
                
    
