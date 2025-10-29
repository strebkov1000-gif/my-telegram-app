from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DB_FILE = 'folders.json'

def load_folders():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_folders(folders):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(folders, f, ensure_ascii=False, indent=2)

# ✅ ДОБАВЬ ЭТОТ ROUTE
@app.route('/')
def home():
    return jsonify({"message": "Telegram Folders API is running!", "status": "ok"})

@app.route('/api/folders', methods=['GET'])
def get_folders():
    folders = load_folders()
    return jsonify(folders)

@app.route('/api/folders', methods=['POST'])
def add_folder():
    try:
        data = request.json
        folders = load_folders()
        
        new_folder = {
            'id': len(folders) + 1,
            'name': data['name'],
            'description': data['description'],
            'channels': data['channels'],
            'author': data.get('author', 'Аноним'),
            'likes': 0,
            'created_at': '2024-01-01'  # временно
        }
        
        folders.append(new_folder)
        save_folders(folders)
        
        return jsonify({'success': True, 'folder': new_folder})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
