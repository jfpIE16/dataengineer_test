# app.py

# Required imports
import os
from flask import Flask, request, jsonify
from google.cloud import firestore
from flask_cors import CORS, cross_origin

# Initialize Flask app
app = Flask(__name__)
cors = CORS(app)
db = firestore.Client()



@app.route('/list', methods=['GET'])
def read():
    try:
        # Check if ID was passed to URL query
        todo_id = request.args.get('id')
        if todo_id:
            client = db.collection('test_bam').where(u'documento', u'==', str(todo_id))
            response = client.stream()
            data = []
            for doc in response:
                data.append(doc.to_dict())
                #print(u'{} => {}'.format(doc.id, doc.to_dict()))
            return jsonify(data, 200)
        else:
            all_todos = {'error': 'Ingrese id de cliente'}
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)