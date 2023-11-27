import speech_recognition


def recognition():
    recognizer = speech_recognition.Recognizer()
    while True:
        with speech_recognition.Microphone() as mic:
            audio_data = recognizer.listen(source=mic)
            text = recognizer.recognize_google(audio_data=audio_data, language='en-US').lower()
            if text == 'On':
                return True
            elif text == 'Off':
                return False

            