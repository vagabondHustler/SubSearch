import os
import sys
import winreg
import socket

from src.config import get
from src.sos import root_directory
from src.sos import root_directory_file
from src.current_user import is_admin
from src.current_user import run_as_admin

COMPUTER_NAME = socket.gethostname()

# write value to "Icon"
def context_menu_icon(use=get("cm_icon")) -> None:
    ss_path = "Directory\Background\shell\SubSearch"
    icon_path = f"{root_directory()}\data\icon.ico, 0"
    with winreg.ConnectRegistry(COMPUTER_NAME, winreg.HKEY_CLASSES_ROOT) as hkey:
        with winreg.OpenKey(hkey, ss_path, 0, winreg.KEY_ALL_ACCESS) as subkey_ss:
            if use == "True":
                winreg.SetValueEx(subkey_ss, "Icon", 0, winreg.REG_SZ, icon_path)
            if use == "False":
                winreg.DeleteValue(subkey_ss, "Icon")


# write value to (Deafult)
def write_command_subkey() -> None:
    from src.config import get

    focus = get("terminal_focus")

    command_path = "Directory\Background\shell\SubSearch\command"

    ppath = os.path.dirname(sys.executable)
    set_title = "import ctypes; ctypes.windll.kernel32.SetConsoleTitleW('SubSearch');"
    set_wd = f"import os; working_path = os.getcwd(); os.chdir('{root_directory()}');"
    run_main = "import main; os.chdir(working_path); main.main()"

    tfocus = f'{ppath}\python.exe -c "{set_title} {set_wd} {run_main}"'
    tsilent = f'{ppath}\pythonw.exe -c "{set_title} {set_wd} {run_main}"'

    with winreg.ConnectRegistry(COMPUTER_NAME, winreg.HKEY_CLASSES_ROOT) as hkey:
        with winreg.OpenKey(hkey, command_path, 0, winreg.KEY_ALL_ACCESS) as subkey_command:
            if focus == "True":
                winreg.SetValueEx(subkey_command, "", 0, winreg.REG_SZ, tfocus)
            elif focus == "False":
                winreg.SetValueEx(subkey_command, "", 0, winreg.REG_SZ, tsilent)


# imports templet registry key to be filled in with values later
def add_context_menu() -> None:
    if is_admin():
        regkey = root_directory_file("data/regkey.reg")
        os.system(f'cmd /c "reg import "{regkey}"')
        context_menu_icon()
        write_command_subkey()
    else:
        run_as_admin()