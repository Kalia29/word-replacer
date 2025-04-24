from flask import Flask, request, jsonify
import base64
import io
from docx import Document

app = Flask(__name__)

@app.route('/replace', methods=['POST'])
def replace_words():
    try:
        data = request.get_json()
        filename = data.get('filename')
        file_b64 = data.get('file')
        replacements = data.get('replacements')

        # Decode base64 content
        file_bytes = base64.b64decode(file_b64)
        file_stream = io.BytesIO(file_bytes)

        # Load Word doc and do replacements
        doc = Document(file_stream)
        for p in doc.paragraphs:
            for old, new in replacements.items():
                if old in p.text:
                    p.text = p.text.replace(old, new)

        # Save updated doc to bytes
        output_stream = io.BytesIO()
        doc.save(output_stream)
        output_stream.seek(0)
        encoded = base64.b64encode(output_stream.read()).decode()

        return jsonify({
            "filename": "updated_" + filename,
            "file": encoded
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
