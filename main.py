from flask import Flask, request, send_file
from docx import Document
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "Word Replacer is running!"

@app.route('/replace', methods=['POST'])
def replace_words():
    file = request.files['file']
    file.save('input.docx')

    word_pairs = request.form.get('replacements')
    if not word_pairs:
        return "No replacements provided", 400

    try:
        replacements = json.loads(word_pairs)
    except:
        return "Invalid JSON", 400

    doc = Document('input.docx')
    for paragraph in doc.paragraphs:
        for old, new in replacements.items():
            if old in paragraph.text:
                paragraph.text = paragraph.text.replace(old, new)

    doc.save('output.docx')
    return send_file('output.docx', as_attachment=True)

app.run(host='0.0.0.0', port=3000)
