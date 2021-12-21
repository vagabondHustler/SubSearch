import requests
import os
import zipfile
import shutil
import struct

from src import log
from src.sos import root_directory_file
from src.sos import cwd

# check if a video is in directory, returns video name without extension
def find_video(cwd_path: str, video_ext: list, with_ext: bool) -> str:
    for file in os.listdir(cwd_path):
        for ext in video_ext:
            if file.endswith(ext):
                video_release_name_ext = file.replace(f"{ext}", "")
                video_release_name = video_release_name_ext.lower()
                if with_ext:
                    return file
                elif with_ext is False:
                    return video_release_name
    return None


# download zip files from url
def download_zip(zip_path: str, zip_url: str, current_num: int, total_num: int) -> None:
    log.output(f"Downloading: {current_num}/{total_num}")
    r = requests.get(zip_url, stream=True)
    with open(zip_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)


# extract all zip file in said directory
def extract_zips(cwd_path: str, extension: str) -> None:
    for file in os.listdir(cwd_path):
        if file.endswith(extension):
            log.output(f"Extracting: {file}")
            file_name = os.path.abspath(file)
            zip_ref = zipfile.ZipFile(file_name)
            zip_ref.extractall(f"{cwd_path}")
            zip_ref.close()


# rename a .srts to the same as video release name
def rename_srts(new_name: str, cwd_path: str, prefered_extension: str, extension: str) -> None:
    for file in os.listdir(cwd_path):
        if file.endswith(prefered_extension) and os.path.exists(new_name) is False:
            log.output(f"Renaming: {file} to {new_name}")
            os.rename(file, new_name)
            return

        elif file.endswith(extension) and os.path.exists(new_name) is False:
            log.output(f"Renaming: {file} to {new_name}")
            os.rename(file, new_name)
            return


# move unused .srts to /subs/
def move_files(cwd_path: str, prefered_extension: str, extension: str) -> None:
    for file in os.listdir(cwd_path):
        file = file.lower()
        if file.endswith(prefered_extension):
            log.output(f"Keeping: {file}")
            continue
        elif file.endswith(extension) and not file.endswith(prefered_extension):
            dir_subs = "subs/"
            os.mkdir(dir_subs) if os.path.exists(dir_subs) is False else None
            log.output(f"Moving: {file} to /subs/")
            os.remove(f"subs/{file}") if os.path.exists(f"subs/{file}") else None
            shutil.move(file, f"subs/{file}")


# remove .zips
def clean_up(cwd_path: str, extension: str) -> None:
    for file in os.listdir(cwd_path):
        if file.endswith(extension):
            log.output(f"Removing: {file}")
            os.remove(file)


def copy_log_to_cwd() -> None:
    file = root_directory_file("search.log")
    dest = f"{cwd()}/search.log"
    shutil.copy(file, dest)


def get_hash(file_name):
    try:
        longlongformat = "<q"  # little-endian long long
        bytesize = struct.calcsize(longlongformat)
        with open(file_name, "rb") as f:
            filesize = os.path.getsize(file_name)
            hash = filesize
            if filesize < 65536 * 2:
                return "SizeError"
            n1 = 65536 // bytesize
            for _x in range(n1):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF  # to remain as 64bit number
            f.seek(max(0, filesize - 65536), 0)
            n2 = 65536 // bytesize
            for _x in range(n2):
                buffer = f.read(bytesize)
                (l_value,) = struct.unpack(longlongformat, buffer)
                hash += l_value
                hash = hash & 0xFFFFFFFFFFFFFFFF

        returnedhash = "%016x" % hash
        return returnedhash

    except IOError as err:
        return log.output(err)