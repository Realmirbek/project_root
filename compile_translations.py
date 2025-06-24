import polib
import os

def compile_mo_from_po(po_path):
    mo_path = po_path.replace(".po", ".mo")
    po = polib.pofile(po_path)
    po.save_as_mofile(mo_path)
    print(f"✅ Compiled: {mo_path}")

def compile_all():
    base_dir = "locales"
    for lang in ["en", "ru"]:
        po_file = os.path.join(base_dir, lang, "LC_MESSAGES", "messages.po")
        if os.path.exists(po_file):
            compile_mo_from_po(po_file)
        else:
            print(f"❌ Not found: {po_file}")

if __name__ == "__main__":
    compile_all()
