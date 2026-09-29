import datetime
import random
import re
import subprocess
import sys
import webbrowser
from urllib.parse import quote_plus

from speech import speak


NOTES_FILE = "notes.txt"


JOKES = [
    "Программист — это устройство для превращения кофе в код.",
    (
        "У оптимиста стакан наполовину полон, "
        "у пессимиста наполовину пуст, "
        "а у программиста индекс выходит за границы массива."
    ),
    (
        "Настоящий программист может назвать "
        "переменную temp2 и жить с этим спокойно."
    ),
    "Есть 10 типов людей: те, кто понимает двоичный код, и те, кто нет.",
    (
        "Самый быстрый способ найти баг — "
        "сказать коллеге, что кода без багов не бывает."
    ),
]



def cmd_time(text):
    now = datetime.datetime.now().strftime("%H:%M")
    speak(f"Сейчас {now}")


def cmd_date(text):
    today = datetime.datetime.now().strftime("%d.%m.%Y")
    speak(f"Сегодня {today}")



def cmd_open_browser(text):
    speak("Открываю браузер")
    webbrowser.open("https://www.google.com")


def cmd_open_youtube(text):
    speak("Открываю Ютуб")
    webbrowser.open("https://www.youtube.com")


def cmd_open_github(text):
    speak("Открываю Гитхаб")
    webbrowser.open("https://github.com")


def cmd_open_chatgpt(text):
    speak("Открываю ChatGPT")
    webbrowser.open("https://chatgpt.com")

def cmd_google_search(text):

    patterns = [
        r"найди в гугле",
        r"погугли",
        r"поищи в гугле",
        r"найди",
        r"поищи",
    ]

    query = text

    for pattern in patterns:
        query = re.sub(
            pattern,
            "",
            query,
            count=1
        )

    query = query.strip()

    if not query:
        speak("Что именно найти?")
        return

    speak(f"Ищу {query}")

    url = (
        "https://www.google.com/search?q="
        + quote_plus(query)
    )

    webbrowser.open(url)


def cmd_youtube_search(text):

    query = re.sub(
        r"^(найди|поищи|включи)",
        "",
        text
    )

    query = re.sub(
        r"\s+на\s+ютубе$",
        "",
        query
    )

    query = query.strip()

    if not query:
        speak("Что найти на Ютубе?")
        return

    speak(f"Ищу на Ютубе {query}")

    url = (
        "https://www.youtube.com/results?search_query="
        + quote_plus(query)
    )

    webbrowser.open(url)



def cmd_wikipedia(text):

    try:
        import wikipedia

    except ImportError:
        speak(
            "Модуль wikipedia не установлен. "
            "Выполните pip install wikipedia"
        )
        return

    wikipedia.set_lang("ru")

    patterns = [
        r"найди в википедии",
        r"расскажи про",
        r"что такое",
        r"кто такой",
        r"кто такая",
    ]

    query = text

    for pattern in patterns:
        query = re.sub(
            pattern,
            "",
            query,
            count=1
        )

    query = query.strip()

    if not query:
        speak("Что искать в Википедии?")
        return

    speak(f"Ищу информацию о {query}")

    try:

        summary = wikipedia.summary(
            query,
            sentences=2
        )

        speak(summary)

    except Exception:
        speak(
            "Не удалось найти информацию "
            "по этому запросу."
        )



def cmd_joke(text):
    speak(random.choice(JOKES))



def cmd_note_add(text):

    note = re.sub(
        r".*запиши заметку",
        "",
        text
    ).strip()

    if not note:
        speak("Что записать?")
        return

    with open(
        NOTES_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(note + "\n")

    speak("Записал")


def cmd_note_read(text):

    try:

        with open(
            NOTES_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            notes = [
                n.strip()
                for n in f.readlines()
                if n.strip()
            ]

    except FileNotFoundError:

        notes = []

    if not notes:
        speak("Заметок пока нет")
        return

    speak(f"У вас {len(notes)} заметок")

    for note in notes:
        speak(note)


def cmd_note_clear(text):

    open(
        NOTES_FILE,
        "w",
        encoding="utf-8"
    ).close()

    speak("Все заметки удалены")


def cmd_calculate(text):

    expression = re.sub(
        r".*(посчитай|вычисли)",
        "",
        text
    ).strip()

    expression = (
        expression
        .replace("плюс", "+")
        .replace("минус", "-")
        .replace("умножить на", "*")
        .replace("умножить", "*")
        .replace("разделить на", "/")
        .replace("разделить", "/")
    )

    expression = expression.strip()

    if not re.fullmatch(
        r"[\d\s.+\-*/()]+",
        expression
    ):
        speak("Не могу распознать выражение")
        return

    try:

        result = eval(
            expression,
            {"__builtins__": {}}
        )

        speak(f"Результат: {result}")

    except Exception:

        speak("Не получилось вычислить пример")



def cmd_open_notepad(text):

    speak("Открываю блокнот")

    if sys.platform.startswith("win"):

        subprocess.Popen(["notepad.exe"])

    elif sys.platform.startswith("darwin"):

        subprocess.Popen(
            ["open", "-a", "TextEdit"]
        )

    else:

        subprocess.Popen(["gedit"])


def cmd_open_calculator(text):

    speak("Открываю калькулятор")

    if sys.platform.startswith("win"):

        subprocess.Popen(["calc.exe"])

    elif sys.platform.startswith("darwin"):

        subprocess.Popen(
            ["open", "-a", "Calculator"]
        )

    else:

        subprocess.Popen(["gnome-calculator"])



def cmd_shutdown_warning(text):

    speak(
        "Команда выключения компьютера "
        "отключена в целях безопасности."
    )



def cmd_help(text):

    speak(
        "Я умею говорить время и дату, "
        "открывать браузер, Ютуб, Гитхаб и ChatGPT, "
        "искать в Гугле и Википедии, "
        "искать видео на Ютубе, "
        "рассказывать анекдоты, "
        "записывать и читать заметки, "
        "считать примеры, "
        "открывать блокнот и калькулятор."
    )



COMMANDS = {

    (
        "сколько времени",
        "который час",
        "который сейчас час",
    ): cmd_time,

    (
        "какое сегодня число",
        "какая сегодня дата",
        "сегодняшняя дата",
    ): cmd_date,

    (
        "открой браузер",
        "запусти браузер",
    ): cmd_open_browser,

    (
        "открой ютуб",
        "открой youtube",
        "запусти ютуб",
    ): cmd_open_youtube,

    (
        "открой гитхаб",
        "открой github",
    ): cmd_open_github,

    (
        "открой чатгпт",
        "открой chatgpt",
        "открой чат gpt",
    ): cmd_open_chatgpt,

    (
        "найди в гугле",
        "погугли",
        "поищи в гугле",
        "найди",
        "поищи",
    ): cmd_google_search,

    (
        "найди на ютубе",
        "поищи на ютубе",
        "найди в ютубе",
        "поищи в ютубе",
    ): cmd_youtube_search,

    (
        "найди в википедии",
        "расскажи про",
        "что такое",
        "кто такой",
        "кто такая",
    ): cmd_wikipedia,

    (
        "расскажи анекдот",
        "пошути",
        "рассмеши меня",
    ): cmd_joke,

    (
        "запиши заметку",
    ): cmd_note_add,

    (
        "прочитай заметки",
        "какие у меня заметки",
        "покажи заметки",
    ): cmd_note_read,

    (
        "удали все заметки",
        "очисти заметки",
    ): cmd_note_clear,

    (
        "посчитай",
        "вычисли",
    ): cmd_calculate,

    (
        "открой блокнот",
        "запусти блокнот",
    ): cmd_open_notepad,

    (
        "открой калькулятор",
        "запусти калькулятор",
    ): cmd_open_calculator,

    (
        "выключи компьютер",
    ): cmd_shutdown_warning,

    (
        "что ты умеешь",
        "помощь",
        "список команд",
    ): cmd_help,
}


def find_command(text: str):

    text = text.lower().strip()

    all_commands = []

    for phrases, handler in COMMANDS.items():

        for phrase in phrases:
            all_commands.append(
                (phrase, handler)
            )

    all_commands.sort(
        key=lambda x: len(x[0]),
        reverse=True
    )

    for phrase, handler in all_commands:

        if phrase in text:
            return handler

    return None