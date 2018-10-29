def open_file_dialog():
    """
    using a tkinter dialog to choose a file
    Returns: the path of a chosen file
    """
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path
