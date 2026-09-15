import datetime
import random
import re
import subprocess
import sys
import webbrowser

from speech import speak

NOTES_FILE = "notes.txt"

JOKES = [
    "Программист - это устройство для превращения кофе в код.",
    "У оптимиста стакан наполовину полон, у пессимиста наполовину пуст, "
    "а у программиста индекс выходит за границы массива.",
    "Настоящий программист может назвать переменную temp2 и жить с этим спокойно.",
    "Есть 10 типов людей: те, кто понимает двоичный код, и те, кто нет.",
    "Самый быстрый способ найти баг — сказать коллеге, что кода без багов не бывает.",
]


# ---------- Время и дата ----------

def cmd_time(text):
    now = datetime.datetime.now().strftime("%H:%M")
    speak(f"Сейчас {now}")


def cmd_date(text):
    today = datetime.datetime.now().strftime("%d.%m.%Y")
    speak(f"Сегодня {today}")


# ---------- Браузер и поиск ----------

def cmd_open_browser(text):
    speak("Открываю браузер")
    webbrowser.open("https://google.com")


def cmd_open_youtube(text):
    speak("Открываю Ютуб")
    webbrowser.open("https://youtube.com")


def cmd_google_search(text):
    query = re.sub(r".*(найди в гугле|погугли|поищи в гугле)", "", text).strip()
    if not query:
        speak("Что именно найти?")
        return
    speak(f"Ищу {query} в Гугле")
    webbrowser.open(f"https://www.google.com/search?q={query}")


def cmd_wikipedia(text):
    try:
        import wikipedia
    except ImportError:
        speak("Модуль wikipedia не установлен. Выполните pip install wikipedia")
        return

    wikipedia.set_lang("ru")
    query = re.sub(r".*(найди в википедии|расскажи про|что такое)", "", text).strip()
    if not query:
        speak("Что искать в Википедии?")
        return

    speak(f"Ищу информацию о {query}")
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except Exception:
        speak("Не удалось найти информацию по этому запросу.")


# ---------- Развлечения ----------

def cmd_joke(text):
    speak(random.choice(JOKES))


# ---------- Заметки ----------

def cmd_note_add(text):
    note = re.sub(r".*запиши заметку", "", text).strip()
    if not note:
        speak("Что записать?")
        return
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(note + "\n")
    speak("Записал")


def cmd_note_read(text):
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = [n.strip() for n in f.readlines() if n.strip()]
    except FileNotFoundError:
        notes = []

    if not notes:
        speak("Заметок пока нет")
        return

    speak("Ваши заметки:")
    for note in notes:
        speak(note)


# ---------- Калькулятор ----------

def cmd_calculate(text):
    expression = re.sub(r".*(посчитай|вычисли)", "", text).strip()
    expression = (
        expression.replace("плюс", "+")
        .replace("минус", "-")
        .replace("умножить на", "*")
        .replace("разделить на", "/")
    )
    # Разрешаем только цифры и математические знаки — никакого произвольного кода
    if not re.fullmatch(r"[\d\s.+\-*/()]+", expression):
        speak("Не могу распознать выражение")
        return
    try:
        result = eval(expression, {"__builtins__": {}})
        speak(f"Результат: {result}")
    except Exception:
        speak("Не получилось вычислить пример")


# ---------- Приложения ----------

def cmd_open_notepad(text):
    speak("Открываю блокнот")
    if sys.platform.startswith("win"):
        subprocess.Popen(["notepad.exe"])
    elif sys.platform.startswith("darwin"):
        subprocess.Popen(["open", "-a", "TextEdit"])
    else:
        subprocess.Popen(["gedit"])


def cmd_open_calculator(text):
    speak("Открываю калькулятор")
    if sys.platform.startswith("win"):
        subprocess.Popen(["calc.exe"])
    elif sys.platform.startswith("darwin"):
        subprocess.Popen(["open", "-a", "Calculator"])
    else:
        subprocess.Popen(["gnome-calculator"])


# ---------- Служебные ----------

def cmd_shutdown_warning(text):
    speak("Команда выключения компьютера отключена в целях безопасности. ")


def cmd_help(text):
    speak(
        "Я умею: говорить время и дату, открывать браузер и Ютуб, "
        "искать в Гугле и Википедии, рассказывать анекдоты, "
        "записывать и читать заметки, считать примеры, "
        "открывать блокнот и калькулятор."
    )


COMMANDS = {
    ("сколько времени", "который час"): cmd_time,
    ("какое сегодня число", "какая сегодня дата"): cmd_date,
    ("открой браузер",): cmd_open_browser,
    ("открой ютуб", "открой youtube"): cmd_open_youtube,
    ("найди в гугле", "погугли", "поищи в гугле"): cmd_google_search,
    ("найди в википедии", "расскажи про", "что такое"): cmd_wikipedia,
    ("расскажи анекдот", "пошути"): cmd_joke,
    ("запиши заметку",): cmd_note_add,
    ("прочитай заметки", "какие у меня заметки"): cmd_note_read,
    ("посчитай", "вычисли"): cmd_calculate,
    ("открой блокнот",): cmd_open_notepad,
    ("открой калькулятор",): cmd_open_calculator,
    ("выключи компьютер",): cmd_shutdown_warning,
    ("что ты умеешь", "помощь", "список команд"): cmd_help,
}


def find_command(text: str):
    """Ищет среди COMMANDS подходящий обработчик по вхождению фразы в текст."""
    for phrases, handler in COMMANDS.items():
        for phrase in phrases:
            if phrase in text:
                return handler
    return None
