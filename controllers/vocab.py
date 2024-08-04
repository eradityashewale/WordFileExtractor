import json
from docx import Document

def extract_vocabulary_data(doc_path):
    doc = Document(doc_path)
    data = []
    entry = {}
    is_in_entry = False

    for para in doc.paragraphs:
        text = para.text.strip()

        # Skip empty lines
        if not text:
            continue

        if text.startswith('1.') or text.startswith('2.'):
            if is_in_entry:
                data.append(entry)
            entry = {"srno": int(text.split('.')[0]), "vocab_name": "", "definition": "", "examples": [], "synonyms": [], "hint": "", "quiz": {"question": "", "options": {}, "correct_option": ""}}
            is_in_entry = True
            vocab_text = text.split(' - ')
            entry["vocab_name"] = vocab_text[0][2:].strip()  # Extracting vocab name
            entry["definition"] = vocab_text[1].strip()
        elif text.startswith('Examples -'):
            continue
        elif text.startswith('Synonyms -'):
            continue
        elif text.startswith('Hint –'):
            entry["hint"] = text[6:].strip()
        elif text.startswith('Quiz -'):
            entry["quiz"]["question"] = text[6:].strip()
        elif text.startswith('a') or text.startswith('b') or text.startswith('c') or text.startswith('d'):
            option = text[0]
            option_text = text[3:].strip()
            entry["quiz"]["options"][option] = option_text
        else:
            # Handling Examples and Synonyms
            if 'Examples -' in text:
                entry["examples"].append(text[len('Examples -'):].strip())
            elif 'Synonyms -' in text:
                entry["synonyms"] = [syn.strip() for syn in text[len('Synonyms -'):].strip().split(',')]

    # Append the last entry
    if is_in_entry:
        data.append(entry)

    return data

def save_to_json(data, json_path):
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"JSON data has been written to '{json_path}'")


