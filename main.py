# main.py
# Точка входа: запускает Джарвиса.
# Цикл работы:
#   1. Слушаем, пока не услышим слово-активатор ("джарвис")
#   2. Говорим "Да, слушаю" и слушаем команду
#   3. Ищем подходящий обработчик и выполняем его

from config import WAKE_WORD, EXIT_WORDS
from speech import speak, listen, setup_voice
from commands import find_command


def main():
    setup_voice()
    speak("Джарвис на связи.")

    while True:
        # Ждём слово-активатор. Короткий phrase_time_limit, чтобы не пропускать реплики.
        text = listen(timeout=None, phrase_time_limit=4)
        if not text or WAKE_WORD not in text:
            continue

        speak("Да, слушаю")
        command_text = listen(timeout=5, phrase_time_limit=6)

        if not command_text:
            speak("Не расслышал, повторите")
            continue

        if any(word in command_text for word in EXIT_WORDS):
            speak("До встречи")
            break

        handler = find_command(command_text)
        if handler:
            handler(command_text)
        else:
            speak("Я не знаю такой команды. Скажите: помощь, чтобы узнать список.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nОстановлено пользователем.")
