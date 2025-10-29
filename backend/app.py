from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Разрешаем запросы из Mini App

# Простая "база данных" в JSON файле
DB_FILE = 'folders.json'


def load_folders():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_folders(folders):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(folders, f, ensure_ascii=False, indent=2)


# API для получения всех папок
@app.route('/api/folders', methods=['GET'])
def get_folders():
    folders = load_folders()
    return jsonify(folders)


# API для добавления новой папки
@app.route('/api/folders', methods=['POST'])
def add_folder():
    data = request.json
    folders = load_folders()

    new_folder = {
        'id': len(folders) + 1,
        'name': data['name'],
        'description': data['description'],
        'channels': data['channels'],
        'author': data.get('author', 'Аноним'),
        'likes': 0,
        'created_at': data['created_at']
    }

    folders.append(new_folder)
    save_folders(folders)

    return jsonify({'success': True, 'folder': new_folder})


if __name__ == '__main__':
    app.run(debug=True)