from config import WAKE_WORD, EXIT_WORDS
from speech import speak, listen, setup_voice
from commands import find_command


def remove_wake_word(text: str) -> str:
    """Убирает слово Джарвис из команды."""

    text = text.lower().strip()

    if WAKE_WORD in text:
        text = text.replace(
            WAKE_WORD,
            "",
            1
        )

    return text.strip()


def is_exit_command(text: str) -> bool:
    """Проверяет команду выхода."""

    text = text.lower().strip()

    for word in EXIT_WORDS:

        if word in text:
            return True

    return False


def main():

    setup_voice()

    speak("Джарвис на связи.")

    while True:


        text = listen(
            timeout=None,
            phrase_time_limit=5
        )

        if not text:
            continue

        if WAKE_WORD not in text:
            continue

        command_text = remove_wake_word(text)


        if is_exit_command(command_text):

            speak("До встречи.")

            break


        if command_text:

            handler = find_command(
                command_text
            )

            if handler:

                handler(command_text)

            else:

                speak(
                    "Я не знаю такой команды. "
                    "Скажите помощь."
                )

            continue


        speak("Да, слушаю.")

        command_text = listen(
            timeout=5,
            phrase_time_limit=6
        )

        if not command_text:

            speak("Не расслышал, повторите.")

            continue


        if is_exit_command(command_text):

            speak("До встречи.")

            break

        handler = find_command(
            command_text
        )

        if handler:

            handler(command_text)

        else:

            speak(
                "Я не знаю такой команды. "
                "Скажите помощь, чтобы узнать список."
            )


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nОстановлено пользователем.")