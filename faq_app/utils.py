from googletrans import Translator

translator = Translator()

def translate_text(text, dest_lang):
    try:
        translation = translator.translate(text, dest=dest_lang)
        return translation.text
    except:
        return text  # Fallback to original text