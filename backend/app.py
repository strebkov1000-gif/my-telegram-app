from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_FILE = 'folders.json'

def load_folders():
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Error loading folders: {e}")
        return []

def save_folders(folders):
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(folders, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving folders: {e}")
        return False

@app.route('/')
def home():
    return jsonify({"message": "Telegram Folders API is running!", "status": "ok"})

@app.route('/api/folders', methods=['GET'])
def get_folders():
    try:
        folders = load_folders()
        return jsonify(folders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/folders', methods=['POST'])
def add_folder():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400
        
        folders = load_folders()
        
        new_folder = {
            'id': len(folders) + 1,
            'name': data.get('name', 'Без названия'),
            'description': data.get('description', 'Описание отсутствует'),
            'channels': data.get('channels', ''),
            'author': data.get('author', 'Аноним'),
            'link': data.get('link', ''),
            'likes': 0,
            'created_at': datetime.now().isoformat()
        }
        
        folders.append(new_folder)
        
        if save_folders(folders):
            return jsonify({'success': True, 'folder': new_folder})
        else:
            return jsonify({'success': False, 'error': 'Failed to save data'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
