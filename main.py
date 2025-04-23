from flask import Flask, request, send_file
from docx import Document
import base64
import io
import json

app = Flask(__name__)

@app.route('/')
def home():
    return 'Word Replacer is running!'

@app.route('/replace', methods=['POST'])
def replace_words():
    data = request.get_json()

    if not data:
        return "Missing JSON body", 400

    filename = data.get('filename')
    file_content = data.get('file')
    replacements = data.get('replacements')

    if not file_content or not replacements:
        return "Missing file content or replacements", 400

    try:
        file_bytes = base64.b64decode(file_content)
        file_stream = io.BytesIO(file_bytes)
        doc = Document(file_stream)
    except Exception as e:
        return f"Failed to read Word doc: {str(e)}", 500

    try:
        for paragraph in doc.paragraphs:
            for old_word, new_word in replacements.items():
                if old_word in paragraph.text:
                    paragraph.text = paragraph.text.replace(old_word, new_word)
    except Exception as e:
        return f"Replacement error: {str(e)}", 500

    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)

    return send_file(output_stream, as_attachment=True, download_name='output.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
