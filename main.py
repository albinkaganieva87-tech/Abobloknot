import tkinter as tk
from tkinter import scrolledtext, filedialog
from tkinter import messagebox
from datetime import datetime
from tkinter import simpledialog
import subprocess
import sys
try:
    from openai import OpenAI
except ModuleNotFoundError:
    # Если библиотеки нет, ставим её через pip скрытно
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    # Пробуем импортировать заново после установки
    from openai import OpenAI


from openai import OpenAI
from tkinter import font
file = ""
current_font_size = 14
is_bold = False
is_italic = False
is_underline = False
is_overstrike = False
current_font_family = "Arial"
current_encoding = "utf-8"

def setenc():
    global current_encoding

    new_enc = simpledialog.askstring(
        "Смена кодировки",
        "Введите кодировку (например: utf-8, cp1251, ascii):",
        initialvalue=current_encoding
    )

    if new_enc:
        new_enc = new_enc.lower().strip()
        try:
            "".encode(new_enc)
            current_encoding = new_enc
            encoding_label.config(text=current_encoding.upper())
            font_label.config(text=current_font_family)
            update_line_style()
        except LookupError:
            messagebox.showerror("Ошибка", f"Кодировка '{new_enc}' не поддерживается Python!")


def update_cursor_position(event=None):
    cursor_index = textArea.index(tk.INSERT)
    line, column = cursor_index.split(".")
    column = int(column) + 1
    cursor_label.config(text=f"Стр {line}, стлб {column}")


def openfile():
    global file
    filepath = filedialog.askopenfilename()
    if filepath:
        file = filepath
        with open(filepath, "r", encoding=f"{current_encoding}") as f:
            text = f.read()
        textArea.delete(1.0, tk.END)
        textArea.insert(1.0, text)
        app.title(f"Abobблокнот - {filepath}")
def update_line_style():
    try:
        start = textArea.index(tk.SEL_FIRST)
        end = textArea.index(tk.SEL_LAST)
    except tk.TclError:
        
        return

    font_effects = []
    if is_bold:
        font_effects.append("bold")
    if is_italic:
        font_effects.append("italic")
    if is_underline:
        font_effects.append("underline")
    if is_overstrike:
        font_effects.append("overstrike")

    textArea.tag_configure(
        "custom_style",
        font=(current_font_family,
              current_font_size,
              " ".join(font_effects))
    )

    textArea.tag_add("custom_style", start, end)
def zh():
    try:
        start = textArea.index(tk.SEL_FIRST)
        end = textArea.index(tk.SEL_LAST)

        if "bold" in textArea.tag_names(start):
            textArea.tag_remove("bold", start, end)
        else:
            textArea.tag_add("bold", start, end)

    except tk.TclError:
        pass

def cursive():
    try:
        start = textArea.index(tk.SEL_FIRST)
        end = textArea.index(tk.SEL_LAST)

        if "italic" in textArea.tag_names(start):
            textArea.tag_remove("italic", start, end)
        else:
            textArea.tag_add("italic", start, end)

    except tk.TclError:
        pass

def setfont_selection():
    try:
        start = textArea.index(tk.SEL_FIRST)
        end = textArea.index(tk.SEL_LAST)
    except tk.TclError:
        return

    new_font = simpledialog.askstring(
        "Смена шрифта",
        "Введите название шрифта:",
        initialvalue=current_font_family
    )

    if not new_font:
        return

    tag_name = f"font_{new_font}"

    textArea.tag_configure(
        tag_name,
        font=(new_font, current_font_size)
    )

    textArea.tag_add(tag_name, start, end)
    
def podch():
    try:
        start = textArea.index(tk.SEL_FIRST)
        end = textArea.index(tk.SEL_LAST)

        if "underline" in textArea.tag_names(start):
            textArea.tag_remove("underline", start, end)
        else:
            textArea.tag_add("underline", start, end)

    except tk.TclError:
        pass

def crest():
    try:
        start = textArea.index(tk.SEL_FIRST)
        end = textArea.index(tk.SEL_LAST)

        if "strike" in textArea.tag_names(start):
            textArea.tag_remove("strike", start, end)
        else:
            textArea.tag_add("strike", start, end)

    except tk.TclError:
        pass
def minus():
    global current_font_size
    if current_font_size > 8:
        current_font_size -= 2
        textArea.configure(font=(current_font_family, current_font_size))
        update_tags()
        zoom_label.config(text=f"{current_font_size}")
        update_line_style()
def plus():
    global current_font_size
    if current_font_size < 72:
        current_font_size += 2
        textArea.configure(font=(current_font_family, current_font_size))
        update_tags()
        zoom_label.config(text=f"{current_font_size}")
        update_line_style()


def setfont():
    global current_font_family
    new_font = simpledialog.askstring(
        "Смена шрифта",
        "Введите название шрифта (Arial, Consolas, Courier, etc, Times New Roman.):",
        initialvalue=current_font_family
    )
    if new_font:
        new_font = new_font.strip()
        current_font_family = new_font
        textArea.configure(font=(current_font_family, current_font_size))
        update_tags()
        font_label.config(text=current_font_family)
        update_line_style()

def saveas():
    global file
    filepath = filedialog.asksaveasfilename(defaultextension=".txt")
    if filepath:
        file = filepath
        with open(filepath, "w", encoding=f"{current_encoding}") as f:
            f.write(textArea.get(1.0, tk.END))
        app.title(f"блокнот - {filepath}")

def save():
    if file:
        with open(file, "w", encoding=f"{current_encoding}") as f:
              f.write(textArea.get(1.0, tk.END))
    else:
        saveas()

def info():
    messagebox.showinfo("справка", "Abobокнот - программа, похожая на блокнот и выполняющая его функции", icon="info")

def clean():
    choice = messagebox.askyesno(
        title="подтверждение",
        message="вы уверены? текст нельзя будет потом вернуть.",
        icon="warning"
    )
    if choice:
        textArea.delete(1.0, tk.END)
        messagebox.showinfo("готово", "текст удален", icon="info")
    else:
        messagebox.showinfo("отмена", "текст  не был удален. причина: отказ рользователя", icon="error")


def update_tags():
    textArea.tag_configure(
        "bold",
        font=(current_font_family, current_font_size, "bold")
    )

    textArea.tag_configure(
        "italic",
        font=(current_font_family, current_font_size, "italic")
    )

    textArea.tag_configure(
        "underline",
        font=(current_font_family, current_font_size)
    )

    textArea.tag_configure(
        "strike",
        font=(current_font_family, current_font_size),
        overstrike=True
    )
app = tk.Tk()
app.title("Abobблокнот")
app.geometry("800x600")
#app.iconbitmap("amogus.ico")
h_scroll = tk.Scrollbar(app, orient="horizontal")
h_scroll.pack(side="bottom", fill="x")

status_bar = tk.Frame(app, bd=1, relief="sunken", bg="#f0f0f0")
status_bar.pack(side="bottom", fill="x")
cell_options = {"side": "left", "padx": 10, "pady": 2}
cursor_label = tk.Label(status_bar, text="Стр 1, стлб 1", bg="#f0f0f0", width=20, anchor="w")
cursor_label.pack(**cell_options)
tk.Label(status_bar, text="|", fg="gray", bg="#f0f0f0").pack(side="left")
zoom_label = tk.Label(status_bar, text=f"{current_font_size}", bg="#f0f0f0", width=8)
zoom_label.pack(**cell_options)
tk.Label(status_bar, text="|", fg="gray", bg="#f0f0f0").pack(side="left")
font_label = tk.Label(status_bar, text=f"{current_font_family}", bg="#f0f0f0", width=15)
font_label.pack(**cell_options)
tk.Label(status_bar, text="|", fg="gray", bg="#f0f0f0").pack(side="left")
line_label = tk.Label(status_bar, text="Windows (CRLF)", bg="#f0f0f0", width=15)
line_label.pack(**cell_options)

tk.Label(status_bar, text="|", fg="gray", bg="#f0f0f0").pack(side="left")
encoding_label = tk.Label(status_bar, text="UTF-8", bg="#f0f0f0", width=10)
encoding_label.pack(**cell_options)
v_scroll = tk.Scrollbar(app)
v_scroll.pack(side="right", fill="y")
textArea = tk.Text(
    app, width=96, height=37,
    xscrollcommand=h_scroll.set,
    yscrollcommand=v_scroll.set,
    wrap="none"
)
textArea.pack(expand=True, fill="both")

# Настройка тегов форматирования
textArea.tag_configure(
    "bold",
    font=(current_font_family, current_font_size, "bold")
)

textArea.tag_configure(
    "italic",
    font=(current_font_family, current_font_size, "italic")
)

textArea.tag_configure(
    "underline",
    underline=True
)

textArea.tag_configure(
    "strike",
    overstrike=True
)
textArea.bind("<KeyRelease>", update_cursor_position)
textArea.bind("<ButtonRelease-1>", update_cursor_position)
update_tags()
def dt():
    date = datetime.now()
    formatteddate = date.strftime("%X %d.%m.%y")
    textArea.insert("end", formatteddate)
    update_cursor_position()
def exit():
    q = messagebox.askyesno("уверены?", "сохранить текст в файл? ", icon="question")
    if q:
        save()
        app.destroy()
    else:
        app.destroy()
def ret():
    global current_font_size
    current_font_size = 14
    textArea.configure(font=(current_font_family, current_font_size))
    zoom_label.config(text=f"{current_font_size}")
    update_line_style()


def ret2():
    global current_font_family, current_font_size, current_zoom
    current_font_family = "Arial"
    current_font_size = 14
    current_zoom = 100
    textArea.configure(font=(current_font_family, current_font_size))
    zoom_label.config(text=f"{current_zoom}%")
    font_label.config(text=current_font_family)
    if 'update_line_style' in globals():
        update_line_style()
def ret3():
    current_encoding = "utf-8"
    encoding_label.config(text=current_encoding.upper())
def full_ret():
    ret()
    ret2()
    ret3()
# Текущий язык по умолчанию
current_lang = "ru"

# Словарь со всеми текстами меню
LOCALIZATION = {
    "ru": {
        "open": "Открыть файл", "save": "Сохранить файл", "saveas": "Сохранить файл как",
        "info": "Справка", "clean": "Очистить", "dt": "Время и дата", "exit": "Выход",
        "enc": "Кодировка", "font": "Шрифт", "bold": "Ж", "italic": "К",
        "strike": "Зачёркнутый", "under": "Подчёркнутый", "basicfont" : "Шрифт по умолч.",
        "basicscale" : "Размер по умолч.", "basicenc" : "Кодровка по умолч.", "basicset" : "Настройки по умолч."
    },
    "en": {
        "open": "Open file", "save": "Save file", "saveas": "Save file as",
        "info": "Help", "clean": "Clear", "dt": "Time and date", "exit": "Exit",
        "enc": "Encoding", "font": "Font", "bold": "B", "italic": "I",
        "strike": "Strikethrough", "under": "Underline", "basicfont" : "Return to Basic font",
        "basicscale" : "Return to basic scale", "basicenc" : "Return to basic enc.", "basicset" : "return to basic set."
    },
    "de": {
        "open": "Datei öffnen", "save": "Datei speichern", "saveas": "Datei speichern unter",
        "info": "Hilfe", "clean": "Löschen", "dt": "Zeit und Datum", "exit": "Beenden",
        "enc": "Kodierung", "font": "Schriftart", "bold": "F", "italic": "K",
        "strike": "Durchgestrichen", "under": "Unterstrichen", "basicfont" : "Standardschriftart",
        "basicscale" : "Standardmaßstab", "basicenc" : "Standardkodierung", "basicset" : "Standardeinstellungen"
    }
}


def set_language():
    global current_lang

    lang_choice = simpledialog.askstring(
        "Язык / Language / Sprache",
        "Введите код языка / Geben Sie den Sprachcode ein / enter a lang. code (ru, en, de):",
        initialvalue=current_lang
    )

    if lang_choice:
        lang_choice = lang_choice.lower().strip()
        if lang_choice in LOCALIZATION:
            current_lang = lang_choice
            update_menu_text()
        else:
            messagebox.showerror("Error", "Language not supported / Язык не поддерживается / Sprache wird nicht unterstützt")
def AI():
    theme = simpledialog.askstring(
        "Язык / Language / Sprache",
        "Введите тему текста, ии сгенерирует его: ",
        initialvalue="амогус"
    )
    
    # Весь код ниже должен быть сдвинут вправо (4 пробела или 1 Tab)
    # чтобы находиться ВНУТРИ функции AI()
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": f"сгенерируй текст про {theme}. без комментариев, просто дай текст"}
        ]
    )
    
    textArea.delete(1.0, tk.END)
    textArea.insert(1.0, response.choices[0].message.content)

menu  = tk.Menu(app, tearoff=0)
def update_menu_text():
    global menu
    menu.delete(0, 'end')

    lang = LOCALIZATION[current_lang]

    menu.add_command(label=lang["open"], command=openfile)
    menu.add_command(label=lang["save"], command=save)
    menu.add_command(label=lang["saveas"], command=saveas)
    menu.add_command(label=lang["info"], command=info)
    menu.add_command(label=lang["clean"], command=clean)
    menu.add_command(label=lang["dt"], command=dt)
    menu.add_command(label=lang["exit"], command=exit)
    menu.add_command(label="+", command=plus)
    menu.add_command(label="-", command=minus)
    menu.add_command(label=lang["enc"], command=setenc)
    menu.add_command(label=lang["font"], command=setfont)
    menu.add_command(label=lang["bold"], command=zh)
    menu.add_command(label=lang["italic"], command=cursive)
    menu.add_command(label=lang["strike"], command=crest)
    menu.add_command(label=lang["under"], command=podch)

    menu.add_command(label="Язык / Language / Sprache", command=set_language)
    menu.add_command(label=lang["basicscale"], command=ret)
    menu.add_command(label=lang["basicfont"], command=ret2)
    menu.add_command(label=lang["basicenc"], command=ret3)
    menu.add_command(label=lang["basicset"], command=ret3)
    menu.add_command(label="AI", command=AI)
update_menu_text()
h_scroll.config(command=textArea.xview)
v_scroll.config(command=textArea.yview)
app.config(menu=menu)
app.mainloop()
