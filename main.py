from flask import Flask, request, jsonify
from docx import Document
import base64
import io

app = Flask(__name__)

@app.route('/')
def home():
    return 'Word Replacer is running!'

@app.route('/replace', methods=['POST'])
def replace_words():
    try:
        data = request.get_json()
        filename = data['filename']
        file_data = base64.b64decode(data['file'])
        replacements = data['replacements']

        doc = Document(io.BytesIO(file_data))

        for p in doc.paragraphs:
            for key, value in replacements.items():
                if key in p.text:
                    p.text = p.text.replace(key, value)

        # Save document to memory
        output_stream = io.BytesIO()
        doc.save(output_stream)
        output_stream.seek(0)
        encoded_result = base64.b64encode(output_stream.read()).decode("utf-8")

        return jsonify({"filename": filename, "file": encoded_result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
