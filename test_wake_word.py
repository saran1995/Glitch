"""
Simple wake word test for debugging
"""
import speech_recognition as sr
import time


def test_wake_word():
    print("🚀 Testing wake word detection independently...")

    recognizer = sr.Recognizer()

    # List microphones
    print("\n🎤 Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  {index}: {name}")

    try:
        # Use default microphone
        microphone = sr.Microphone()

        print("\n🔧 Adjusting for ambient noise (please be quiet)...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)

        print(f"✅ Ready! Energy threshold: {recognizer.energy_threshold}")
        print("👂 Say 'Hey Glitch' or 'Glitch' (or anything to test)...")
        print("Press Ctrl+C to stop")

        while True:
            try:
                with microphone as source:
                    # Listen for audio
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)

                    # Try to recognize
                    text = recognizer.recognize_google(audio).lower()
                    print(f"🎯 Heard: '{text}'")

                    # Check for wake words
                    if "glitch" in text:
                        print(f"🚨 WAKE WORD DETECTED: {text}")

            except sr.WaitTimeoutError:
                print(".", end="", flush=True)  # Show it's listening
            except sr.UnknownValueError:
                print("?", end="", flush=True)  # Couldn't understand
            except sr.RequestError as e:
                print(f"\n❌ Speech recognition error: {e}")
                break
            except KeyboardInterrupt:
                print("\n👋 Test stopped by user")
                break

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_wake_word()
