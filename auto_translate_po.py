import polib
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

def translate_text(text, target='ru'):
    if not text.strip():
        return text
    result = translate_client.translate(text, target_language=target)
    return result['translatedText']

def auto_translate_po(input_po_path, output_po_path, target_lang='ru'):
    po = polib.pofile(input_po_path)

    for entry in po:
        if not entry.translated() and entry.msgid.strip():
            translated = translate_text(entry.msgid, target=target_lang)
            entry.msgstr = translated
            print(f"Translated: {entry.msgid} -> {translated}")

    po.save(output_po_path)
    print(f"Saved translated PO: {output_po_path}")

if __name__ == '__main__':
    input_po = 'locales/en/LC_MESSAGES/messages.po'  # Английский исходник
    output_po = 'locales/ru/LC_MESSAGES/messages.po'  # Русский с переводами
    auto_translate_po(input_po, output_po, 'ru')
