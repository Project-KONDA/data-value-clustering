'''Windows filedialog to save and load json files and save excel files'''
from tkinter import filedialog


def getJsonLoadPath(initial_dir=None):
    if initial_dir is None:
        initial_dir = "../"
    file_name = filedialog.askopenfilename(
        initialdir=initial_dir,
        title="Load File",
        filetypes=(("Json Files", "*.json"),
                   ("All Files", "*.*"))
    )
    return file_name


def getJsonSavePath(initial_dir=None):
    if initial_dir is None:
        initial_dir = "../"
    file_name = filedialog.asksaveasfilename(
        initialdir=initial_dir,
        title="Save File",
        filetypes=(("Json Files", "*.json"),
                   ("All Files", "*.*"))
    )
    if file_name is not None and file_name != "" and not file_name.endswith(".json"):
        file_name = file_name + ".json"
    if file_name == "":
        file_name = None
    return file_name


def getExcelSavePath():
    file_name = filedialog.asksaveasfilename(
        initialdir="../",
        title="Save File",
        filetypes=(("Excel Files", "*.xlsx"),
                   ("All Files", "*.*"))
    )
    if file_name is not None and file_name != "" and not file_name.endswith(".xlsx"):
        file_name = file_name + ".xlsx"
    if file_name == "":
        file_name = None
    return file_name


def getOpenFilePath(title):
    file_name = filedialog.askopenfilename(title=title)
    return file_name


if __name__ == '__main__':
    path = getJsonLoadPath()
    print(path)
    path = getJsonSavePath()
    print(path)
    path = getExcelSavePath()
    print(path)
