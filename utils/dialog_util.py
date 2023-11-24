import tkinter as tk
from tkinter import filedialog

FILE_TYPES = {
    "txt": ("Text Files", ".txt"),
    "image": ("Image Files", ".png .jpg .gif .jpeg"),
    "pdf": ("PDF Files", ".pdf"),
    "excel": ("Excel Files", ".xlsx .xls"),
    "xmind": ("XMind Flies", ".xmind"),
    "sql": ("SQL Files", ".sql")
}


def browse_file(*file_types: str) -> str:
    """
    调用窗口选择文件，返回文件路径
    :param file_types:
        文件类型，可选："txt","image","pdf","excel","xmind","sql"；
        不传时，默认所有文件类型可选择
    """
    filetypes = [
        FILE_TYPES[t]
        for t in file_types if t in FILE_TYPES
    ]

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="选择文件",
        filetypes=filetypes
    )

    return file_path
