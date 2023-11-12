import os
import time

from colorama import Fore, init
from natsort import os_sorted
from exif import Image

path_start = r"C:\Users\USERNAME\Desktop"
extensions = (
    '.jpg', '.jpeg', '.jpe' '.jif', '.jfif', '.jfi', '.tif', '.tiff',
    '.JPG', '.JPEG', '.JPE' '.JIF', '.JFIF', '.JFI', '.TIF', '.TIFF'
)

init()


def find_directory() -> str:
    return input('Desktop directory name: ').strip()


def sort_n_remove(files) -> list:
    return [f for f in os_sorted(files) if str(f).endswith(extensions)]


def rename(files, path, quantity):
    print("Renaming files...\n")
    renamed = 0
    progress_bar(renamed, quantity)
    for index, name in enumerate(files, start=1):
        extension = os.path.splitext(name)[1]
        old_path = os.path.join(path, name)
        new_path = os.path.join(path, f"{index}{extension}")
        os.rename(old_path, new_path)

        renamed += 1
        progress_bar(renamed, quantity)

    print(Fore.GREEN + f"{renamed}/{quantity} files have been renamed" + Fore.RESET)


def add_exif(files, path, quantity):
    print("Editing the EXIF metadata...\n")
    edited = 0
    progress_bar(edited, quantity)
    for index, name in enumerate(files):
        with open(os.path.join(path, name), 'rb') as file:
            image = Image(file)
            author = "author"
            image.set("artist", author)
        with open(os.path.join(path, f"{os.path.splitext(name)[0]}exif{os.path.splitext(name)[1]}"), 'wb') as file:
            file.write(image.get_file())

        edited += 1
        progress_bar(edited, quantity)


def clear_last_line():
    print('\033[1A', end='\x1b[2K')


def progress_bar(done, quantity):
    percent = int(done / quantity * 100)
    scale = 2
    adjusted_percent = int(percent / scale)
    adjusted_maximum = int(100 / scale)
    clear_last_line() if percent != 0 else None
    print(Fore.BLUE + f"{done}/{quantity} ({percent}%)  " + Fore.MAGENTA +
          f"[{'-' * adjusted_percent}{' ' * (adjusted_maximum - adjusted_percent)}]" + Fore.RESET)

    # just for the process to be more visual :)
    time.sleep(0.1)


def main():
    # find the path and retrieve the files
    while True:
        try:
            path = os.path.join(path_start, find_directory())
            files = os.listdir(path)
            break
        except FileNotFoundError:
            print(Fore.RED + "This directory was not found. Please, try again." + Fore.RESET)

    # sort the files (ascending order) and remove the non-image files
    sorted_files = sort_n_remove(files)
    quantity = len(sorted_files)
    print(f"Total: {quantity} pictures\n")

    # ask what needs doing (rename, add EXIF, or both)
    to_do = int(input(
        "Choose a mode:\n"
        "1 - rename the files\n"
        "2 - add EXIF metadata to the files\n"
        "3 - do both\n"
    ).strip())
    # remove the input (just for the looks)
    clear_last_line()

    if to_do == 1:
        # change the file names to corresponding integer indexes starting from 1
        rename(sorted_files, path, quantity)
    elif to_do == 2:
        # edit the EXIF metadata of the files
        print(f"{add_exif(sorted_files, path, quantity)}/{quantity} files have got their metadata modified")
    elif to_do == 3:
        rename(sorted_files, path, quantity)
        files = os.listdir(path)
        sorted_files = sort_n_remove(files)
        quantity = len(sorted_files)
        print(f"{add_exif(sorted_files, path, quantity)}/{quantity} files have got their metadata modified")


main()
