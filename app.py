from flask import Flask, request, jsonify
from unstructured.partition.auto import partition
import base64
import tempfile
import os

app = Flask(__name__)

MIME_TO_EXT = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/extract', methods=['POST'])
def extract_text():
    try:
        data = request.json
        if not data or 'file' not in data:
            return jsonify({"error": "Missing file", "success": False}), 400
        
        file_b64 = data['file']
        mime_type = data.get('mimeType', 'application/pdf')
        file_name = data.get('fileName', 'unknown')
        extension = MIME_TO_EXT.get(mime_type, '.bin')
        
        file_data = base64.b64decode(file_b64)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
            tmp.write(file_data)
            tmp_path = tmp.name
        
        elements = partition(filename=tmp_path)
        text = "\n\n".join([str(el) for el in elements])
        os.remove(tmp_path)
        
        return jsonify({
            "text": text,
            "fileName": file_name,
            "success": True
        }), 200
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
