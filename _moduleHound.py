from pip import main

def sniff(module=None): # Passing none will sniff all required modules
    if module and not isinstance(module, str): return

    allmod = module is None

    print(f"Sniffing for {'all modules' if allmod else module}...")

    if allmod or module == "gtts":
        try:
            import gtts
        except:
            main(["install", "gtts"])

    if allmod or module == "mutagen":
        try:
            import mutagen
        except:
            main(["install", "mutagen"])

    if allmod or module == "SR":
        try:
            import speech_recognition
        except:
            main(["install", "SpeechRecognition"])

    print("Done!")


if __name__ == "__main__":
    sniff()