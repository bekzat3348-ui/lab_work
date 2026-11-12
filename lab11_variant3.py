import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Выдача книг")
root.geometry("720x500")
root.minsize(620, 420)

reader_var = tk.StringVar()
book_var = tk.StringVar(value="Python для начинающих")
status_var = tk.StringVar(value="Готово")
count_var = tk.StringVar(value="Книг на руках: 0")

books = [
    "Python для начинающих",
    "Основы программирования",
    "Алгоритмы и структуры данных",
    "Базы данных",
    "Искусственный интеллект"
]
issued_books = []

frame = ttk.Frame(root, padding=15)
frame.pack(fill="both", expand=True)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)

ttk.Label(frame, text="Имя читателя").grid(row=0, column=0, sticky="w", pady=6)
reader_entry = ttk.Entry(frame, textvariable=reader_var)
reader_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=8, pady=6)

ttk.Label(frame, text="Книга").grid(row=1, column=0, sticky="w", pady=6)
book_box = ttk.Combobox(frame, textvariable=book_var, values=books, state="readonly")
book_box.grid(row=1, column=1, columnspan=2, sticky="ew", padx=8, pady=6)

issue_button = ttk.Button(frame, text="Выдать книгу")
issue_button.grid(row=2, column=1, sticky="ew", padx=5, pady=8)
clear_button = ttk.Button(frame, text="Очистить список")
clear_button.grid(row=2, column=2, sticky="ew", padx=5, pady=8)

result_list = tk.Listbox(frame, height=12)
result_list.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=8)

ttk.Label(frame, textvariable=count_var).grid(row=4, column=0, sticky="w")
ttk.Label(frame, text="Дважды щелкните запись, чтобы отметить возврат").grid(
    row=5, column=0, columnspan=3, sticky="w", pady=5
)
ttk.Label(frame, textvariable=status_var).grid(row=4, column=1, columnspan=2, sticky="e")


def reset_status():
    status_var.set("Готово")


def set_status(message):
    status_var.set(message)
    root.after(2500, reset_status)


def update_count():
    active_count = sum(1 for item in issued_books if not item["returned"])
    count_var.set(f"Книг на руках: {active_count}")


def refresh_list():
    result_list.delete(0, tk.END)
    for item in issued_books:
        state = "Возвращена" if item["returned"] else "На руках"
        result_list.insert(tk.END, f'{item["reader"]} — {item["book"]} ({state})')


def issue_book():
    reader = reader_var.get().strip()
    book = book_var.get()

    if len(reader) < 2:
        messagebox.showwarning("Проверка", "Введите имя читателя (не менее 2 символов)")
        reader_entry.focus_set()
        return

    for item in issued_books:
        same_reader = item["reader"].casefold() == reader.casefold()
        if same_reader and item["book"] == book and not item["returned"]:
            set_status("Эта книга уже выдана этому читателю")
            return

    issued_books.append({"reader": reader, "book": book, "returned": False})
    refresh_list()
    update_count()
    set_status("Книга выдана")
    reader_var.set("")
    reader_entry.focus_set()


def mark_returned(event=None):
    selected = result_list.curselection()
    if not selected:
        set_status("Сначала выберите запись")
        return

    index = selected[0]
    item = issued_books[index]
    if item["returned"]:
        set_status("Книга уже отмечена как возвращённая")
        return

    item["returned"] = True
    refresh_list()
    result_list.selection_set(index)
    update_count()
    set_status("Возврат книги отмечен")


def on_double_click(event):
    mark_returned()


def clear_all():
    if not issued_books:
        set_status("Список уже пуст")
        return

    answer = messagebox.askyesno("Подтверждение", "Удалить все записи о выдаче книг?")
    if answer:
        issued_books.clear()
        refresh_list()
        update_count()
        set_status("Список очищен")


issue_button.config(command=issue_book)
clear_button.config(command=clear_all)
reader_entry.bind("<Return>", lambda event: issue_book())
result_list.bind("<Double-Button-1>", on_double_click)

reader_entry.focus_set()
root.mainloop()
