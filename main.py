from flask import Flask, request, jsonify
from docx import Document
import base64
import io
import os

app = Flask(__name__)

@app.route('/replace', methods=['POST'])
def replace_words():
    try:
        # Get data from the request
        data = request.get_json()
        filename = data.get('filename')
        file_content = data.get('file')
        replacements = data.get('replacements')

        # Decode the base64 file
        decoded_file = base64.b64decode(file_content)
        docx_file = io.BytesIO(decoded_file)

        # Load and process the Word document
        doc = Document(docx_file)
        for p in doc.paragraphs:
            for old, new in replacements.items():
                if old in p.text:
                    p.text = p.text.replace(old, new)

        # Save updated file to memory
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        encoded_output = base64.b64encode(output.read()).decode('utf-8')

        return jsonify({
            'filename': filename,
            'updated_file': encoded_output
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Required for Render to detect the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
