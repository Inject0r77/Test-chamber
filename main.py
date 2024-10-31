# main.py
import tkinter as tk
import ctypes
from proxy_generator.gui import create_gui

def hide_console():
    """Скрытие консольного окна."""
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def main():
    """Запуск главного приложения."""
    hide_console()  # Скрыть консоль
    root = tk.Tk()
    root.title("Генератор прокси")

    # Создание графического интерфейса
    create_gui(root)

    # Запуск основного цикла приложения
    root.mainloop()

if __name__ == "__main__":
    main()
