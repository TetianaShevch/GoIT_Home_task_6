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
from pathlib import Path
import shutil
import re
import sort

# python main.py Rubbish 

folder_to_scan = sys.argv[1]
# folder_to_scan = 'Rubbish'
          
sort.read_folder(Path(folder_to_scan), Path(folder_to_scan)) # Обробляємо директорію

sort.handle_empty_folders(Path(folder_to_scan)) # після сортування файлів у директорії видаляємо пусті папки, що утворилися після упорядкування, і нормалізуємо назви файлів

# Друкуємо список файлів у категорії (музика, відео, фото та ін.)
print(f'Images: {sort.images}') 
print(f'Video: {sort.video}')
print(f'Documents: {sort.documents}')
print(f'Audio: {sort.audio}')
print(f'Archives: {sort.archives}')
print(f'Other files: {sort.my_others}')
# Друкуєхмо перелік всіх відомих скриптів розширень, які зустрічаються в цільовій папці.
print(f'Types of files in folder: {sort.EXTENSION}')
# Друкуємо перелік усіх розширень, які скрипту невідомі.
print(f'Files of Unknown types: {sort.unknown}')

