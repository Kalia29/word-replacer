from flask import Flask, request, jsonify
from docx import Document
import base64
import io
import json
import zipfile
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return 'Word Replacer is running!'

@app.route('/replace', methods=['POST'])
def replace_words():
    try:
        data = request.get_json()
        print("Incoming JSON:", data)

        filename = data.get('filename', 'output.docx')
        file_data = data.get('file')
        replacements = data.get('replacements', {})

        if isinstance(replacements, str):
            replacements = json.loads(replacements)

        if not file_data:
            return jsonify({"error": "Missing file content"}), 400

        # Decode base64 and load as Word document
        file_bytes = base64.b64decode(file_data)
        try:
            doc = Document(io.BytesIO(file_bytes))
        except zipfile.BadZipFile:
            print("Invalid .docx file: not a ZIP")
            return jsonify({"error": "Uploaded file is not a valid .docx file"}), 400

        # Replace text in paragraphs
        for p in doc.paragraphs:
            for key, value in replacements.items():
                if key in p.text:
                    p.text = p.text.replace(key, value)

        output_stream = io.BytesIO()
        doc.save(output_stream)
        output_stream.seek(0)
        encoded_result = base64.b64encode(output_stream.read()).decode("utf-8")

        return jsonify({"filename": filename, "file": encoded_result})

    except Exception as e:
        print("ERROR:", traceback.format_exc())
        return jsonify({"error": traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
