'''
Завдання: Сортування файлів у папці.

Перенести файли із зазначеної папки в нову папку з розширенням цього файлу:
зображення переносимо до папки images
документи переносимо до папки documents
аудіо файли переносимо в audio
відео файли у video
архіви розпаковуються та їх вміст переноситься до папки archives
'''
import sys
import argparse
from pathlib import Path
from shutil import move
import re

# python main.py -s Rabbish 
# -s - source

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('--source', '-s', required=True, help='Source folder')
folder_to_scan = sys.argv[1]
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
    'ZIP': archives,
    'GZ': archives, 
    'TAR': archives
}
EXTENSION = set()
print(f'Start in folder {folder_to_scan}')
read_folder(Path(folder_to_scan))
print(f'Images: {images}')
print(f'Video: {video}')
print(f'Documents: {documents}')
print(f'Audio: {audio}')
print(f'Archives: {archives}')
print(f'Types of files in folder: {EXTENSION}')
print(f'Files of Unknown types: {unknown}')
print(f'MY_OTHER: {my_others}')

def read_folder(path: Path) -> None:
    for el in path.iterdir():
        el = normalize(el)
        if el.is_dir():
            if el.name not in ('archives', 'video', 'audio', 'documents', 'images', 'my_others'):
                read_folder(el)
            continue 
        else:
            move_file(el)

def normalize(element: str) -> str:
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    element_trans = element.translate(TRANS)
    element_trans = re.sub(r'\W', '_', element_trans)
    return element_trans

def move_file(file: Path):
    ext = file.suffix.upper()   
    if not ext:  
        my_others.append(file)
    else:
        try:
            container = REGISTER_EXTENSION[ext]
            EXTENSION.add(ext)
            container.append(file)
        except KeyError:
            unknown.add(ext)
            my_others.append(file)
    # images = []
    # documents = []
    # audio = []
    # video = []
    # archives = []
    # unknown = []
    # my_others = []
    # REGISTER_EXTENSION = {
    #     'JPEG': images,
    #     'JPG': images,
    #     'PNG': images,
    #     'SVG': images,
    #     'AVI': video, 
    #     'MP4': video, 
    #     'MOV': video, 
    #     'MKV': video,
    #     'DOC': documents, 
    #     'DOCX': documents,
    #     'TXT': documents, 
    #     'PDF': documents, 
    #     'XLSX': documents, 
    #     'PPTX': documents,
    #     'MP3': audio,
    #     'OGG': audio, 
    #     'WAV': audio, 
    #     'AMR': audio,
    #     'ZIP': archives,
    #     'GZ': archives, 
    #     'TAR': archives
    # }
    # EXTENSION = set()
    

# if __name__ == "__main__":
#     folder_to_scan = sys.argv[1]
#     print(f'Start in folder {folder_to_scan}')
#     read_folder(Path(folder_to_scan))
#     print(f'Images: {images}')
#     print(f'Video: {video}')
#     print(f'Documents: {documents}')
#     print(f'Audio: {audio}')
#     print(f'Archives: {archives}')​
#     print(f'Types of files in folder: {EXTENSION}')
#     print(f'Unknown files of types: {unknown}')
#     print(f'MY_OTHER: {my_others}')

