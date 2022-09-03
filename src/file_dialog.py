from tkinter import Tk, filedialog
from pathlib import Path

def initiate_tk_dialog():
    root = Tk()  # pointing root to Tk() to use it as Tk() in program.
    root.withdraw()  # Hides small tkinter window.
    root.attributes('-topmost', True)  # Opened windows will be active. above all windows despite of selection.
    return root

def get_data_file(title: str, as_path = False):
    """Open windows dialog to select file. Return file path.
    title: string to show on top of windows dialog
    as_path: Return file location as Path (as_path = True).
             as_path = False returns string.
    """
    root = initiate_tk_dialog()
    if as_path == True:
        data_file: Path = Path(filedialog.askopenfilename(title= title))  # Returns opened path as str
    else:
        data_file: str = str(filedialog.askopenfilename(title= title)) 
    root.destroy()
    return data_file

def get_directory(title: str, as_path = False):
    """Open windows dialog to select directory. Return directory path.
    title: string to show on top of windows dialog
    as_path: Return file location as Path (as_path = True).
             as_path = False returns string.
    """
    root = initiate_tk_dialog()
    if as_path == True:
        directory: Path = Path(filedialog.askdirectory(title= title))
    else:
        directory: str = str(filedialog.askdirectory(title= title))
    root.destroy()
    return directory
