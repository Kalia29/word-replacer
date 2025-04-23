from flask import Flask, request, jsonify
import base64
from io import BytesIO
from docx import Document

app = Flask(__name__)

@app.route('/replace', methods=['POST'])
def replace_words():
    try:
        data = request.get_json()

        # Step 1: Get fields
        filename = data.get('filename', 'Output.docx')
        replacements = data.get('replacements', {})
        file_b64 = data.get('file')

        if not file_b64:
            return jsonify({"error": "Missing file content"}), 400

        # Step 2: Decode and load Word document
        file_bytes = base64.b64decode(file_b64)
        doc = Document(BytesIO(file_bytes))

        # Step 3: Replace text
        for paragraph in doc.paragraphs:
            for key, val in replacements.items():
                if key in paragraph.text:
                    paragraph.text = paragraph.text.replace(key, val)

        # Step 4: Save to memory
        output_stream = BytesIO()
        doc.save(output_stream)
        output_b64 = base64.b64encode(output_stream.getvalue()).decode('utf-8')

        # Step 5: Return result
        return jsonify({
            "filename": f"Updated_{filename}",
            "file": output_b64
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Keep the app running on port 3000 for Render
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
