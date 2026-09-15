import asyncio
import os
import tempfile

import speech_recognition as sr
import pyttsx3

from config import LANGUAGE, SPEECH_RATE, EDGE_VOICE

recognizer = sr.Recognizer()
engine = pyttsx3.init()

try:
    import edge_tts
    from playsound import playsound
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False


def setup_voice():
    """Настраивает резервный голос pyttsx3 (используется, если edge-tts недоступен)."""
    voices = engine.getProperty("voices")
    for voice in voices:
        name = (voice.name or "").lower()
        vid = (voice.id or "").lower()
        if "russian" in name or "ru" in vid or "irina" in name:
            engine.setProperty("voice", voice.id)
            break
    engine.setProperty("rate", SPEECH_RATE)


def _speak_pyttsx3(text: str):
    engine.say(text)
    engine.runAndWait()


async def _speak_edge_tts(text: str):
    communicate = edge_tts.Communicate(text, EDGE_VOICE)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        temp_path = f.name
    try:
        await communicate.save(temp_path)
        playsound(temp_path)
    finally:
        os.remove(temp_path)


def speak(text: str):
    """Озвучивает текст. Сначала пробует edge-tts (лучше качество),
    при любой ошибке (нет сети, сбой) — переключается на pyttsx3."""
    print(f"Джарвис: {text}")

    if EDGE_TTS_AVAILABLE:
        try:
            asyncio.run(_speak_edge_tts(text))
            return
        except Exception as e:
            print(f"edge-tts недоступен ({e}), перехожу на резервный голос")

    _speak_pyttsx3(text)


def listen(timeout=None, phrase_time_limit=5) -> str:
    """Слушает микрофон и возвращает распознанный текст в нижнем регистре.
    timeout=None означает "ждать бесконечно, пока не начнут говорить".
    phrase_time_limit — максимальная длина одной фразы в секундах."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio, language=LANGUAGE)
        print(f"Вы сказали: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Проблема с подключением к сервису распознавания речи.")
        return ""