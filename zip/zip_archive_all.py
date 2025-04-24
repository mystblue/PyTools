import os
import shutil

def main():
    files = os.listdir('.')
    for file in files:
         if os.path.isdir(file):
             shutil.make_archive(file, format='zip', root_dir='.', base_dir=file)

if __name__ == '__main__':
    main()
