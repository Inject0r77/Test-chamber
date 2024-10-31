# proxy_generator/gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from proxy_generator.proxy import generate_proxies, validate_proxy
import threading
import pyfiglet

def create_gui(root: tk.Tk) -> None:
    """
    Создание графического интерфейса.
    
    :param root: Главное окно приложения.
    """
    def on_generate():
        """Обработка нажатия кнопки генерации прокси в отдельном потоке."""
        threading.Thread(target=generate_proxies_thread).start()

    def generate_proxies_thread():
        """Функция для генерации прокси в отдельном потоке."""
        country = country_var.get()
        quantity = quantity_entry.get()
        save_path = save_path_var.get()
        
        if not country or not quantity.isdigit() or not save_path:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля правильно.")
            return
        
        quantity = int(quantity)
        log_text.delete(1.0, tk.END)  # Очистка текстового поля логов
        log("Начинаем генерацию прокси...")
        
        proxies = generate_proxies(country, quantity)

        # Сохранение прокси в файл и отображение статуса
        with open(save_path, 'w') as file:
            for proxy in proxies:
                is_valid = validate_proxy(proxy)
                status = "[ВАЛИД]" if is_valid else "[НЕВАЛИД]"
                color = "green" if is_valid else "red"
                
                # Запись прокси в файл
                file.write(f"{proxy}\n")
                
                # Логирование в GUI
                log(f"{status} {proxy}", color=color)

        log(f"Сгенерировано {len(proxies)} прокси и сохранено в {save_path}")

    def log(message: str, color: str = "black") -> None:
        """
        Логирование сообщений в текстовом поле.
        
        :param message: Сообщение для логирования.
        :param color: Цвет текста для сообщения.
        """
        log_text.insert(tk.END, message + "\n")
        log_text.tag_add("color", log_text.index("end - 1 chars"), log_text.index("end"))
        log_text.tag_config("color", foreground=color)

    # Переменные
    country_var = tk.StringVar()
    save_path_var = tk.StringVar()

    # Заголовок с ASCII-артом
    ascii_art = pyfiglet.figlet_format("Test program by #Aqumarine")
    title_label = tk.Label(root, text=ascii_art, font=("Courier", 14), justify=tk.LEFT)
    title_label.pack()

    # Выбор страны
    country_label = tk.Label(root, text="Выберите страну:")
    country_label.pack()

    # Создание выпадающего списка для выбора страны
    countries = ["Россия", "США", "Канада", "Германия", "Франция"]
    country_combo = ttk.Combobox(root, textvariable=country_var, values=countries)
    country_combo.pack()
    country_combo.current(0)  # Установка значения по умолчанию

    # Ввод количества прокси
    quantity_label = tk.Label(root, text="Количество прокси:")
    quantity_label.pack()
    
    quantity_entry = tk.Entry(root)
    quantity_entry.pack()

    # Кнопка выбора места сохранения
    save_button = tk.Button(root, text="Выбрать место сохранения", command=lambda: save_path_var.set(filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Текстовые файлы", "*.txt")])))
    save_button.pack()

    # Кнопка генерации
    generate_button = tk.Button(root, text="Сгенерировать прокси", command=on_generate)
    generate_button.pack()

    # Поле для логирования
    log_text = tk.Text(root, height=10, width=50)
    log_text.pack()
    log_text.config(state=tk.NORMAL)
