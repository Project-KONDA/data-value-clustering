'''Windows filedialog to save and load json files and save excel files'''
from tkinter import filedialog


def getJsonLoadPath():
    file_name = filedialog.askopenfilename(
        initialdir="../",
        title="Load File",
        filetypes=(("Json Files", "*.json"),
                   ("All Files", "*.*"))
    )
    return file_name


def getJsonSavePath():
    file_name = filedialog.asksaveasfilename(
        initialdir="../",
        title="Save File",
        filetypes=(("Json Files", "*.json"),
                   ("All Files", "*.*"))
    )
    if file_name and not file_name.endswith(".json"):
        file_name = file_name + ".json"
    return file_name


def getExcelSavePath():
    file_name = filedialog.asksaveasfilename(
        initialdir="../",
        title="Save File",
        filetypes=(("Excel Files", "*.xlsx"),
                   ("All Files", "*.*"))
    )
    if file_name and not file_name.endswith(".xlsx"):
        file_name = file_name + ".xlsx"
    return file_name


if __name__ == '__main__':
    path = getJsonLoadPath()
    print(path)
    path = getJsonSavePath()
    print(path)
    path = getExcelSavePath()
    print(path)
