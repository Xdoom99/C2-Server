import os
import shutil
import random
import string

# Define constants
FILE_TO_COPY = 'winplant.py'
FILE_NAME_LENGTH = 6

# Get the current working directory
current_directory = os.getcwd()

# Generate a random file name
random_filename = ''.join(random.choices(string.ascii_lowercase, k=FILE_NAME_LENGTH)) + '.py'

# Construct the full path of the file to copy
file_to_copy_path = os.path.join(current_directory, FILE_TO_COPY)

if os.path.exists(file_to_copy_path):
    shutil.copy(file_to_copy_path, random_filename)
    print(f'[+] {FILE_TO_COPY} copied to {random_filename}')
else:
    print(f'[-] {FILE_TO_COPY} file not found')
