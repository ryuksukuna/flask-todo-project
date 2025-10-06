from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import uuid
import hashlib

app = Flask(__name__)

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['todo_database']
todo_collection = db['todo_items']

# Sample initial data
sample_data = {
    "project": "Todo Application",
    "version": "1.0",
    "items": [
        {"id": 1, "name": "Initial Task", "description": "Setup project structure"}
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api')
def api():
    return jsonify(sample_data)

@app.route('/todo')
def todo_page():
    return render_template('todo.html')

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    try:
        data = request.get_json()
        
        # Generate additional fields
        item_id = data.get('itemId')
        item_uuid = str(uuid.uuid4())
        item_hash = hashlib.md5(f"{data.get('itemName')}{item_id}".encode()).hexdigest()
        
        item_data = {
            'itemId': item_id,
            'itemName': data.get('itemName'),
            'itemDescription': data.get('itemDescription'),
            'itemUUID': item_uuid,
            'itemHash': item_hash
        }
        
        # Insert into MongoDB
        result = todo_collection.insert_one(item_data)
        
        return jsonify({
            'message': 'Todo item added successfully!',
            'inserted_id': str(result.inserted_id),
            'generated_uuid': item_uuid,
            'generated_hash': item_hash
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
