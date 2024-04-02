from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate


from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET','POST'])
def messages():

    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            message_dict = message.to_dict()
            messages.append(message_dict)
        response = make_response(messages,200)
        return response
    
    elif request.method == 'POST':
        message_data = request.json
        new_message = Message(
        body = message_data.get('body'),
        username = message_data.get('username')
        )
        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict() 
        return make_response(new_message_dict,201)


@app.route('/messages/<int:id>', methods = ['GET','PATCH','DELETE'])
def messages_by_id(id):
    
    message = Message.query.filter(Message.id == id).first()
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    if request.method == 'GET':
        message_dict = message.to_dict()
        response = make_response(message_dict,200)
        return response
        
    elif request.method == 'PATCH':
        message_data = request.json
        body = message_data.get('body')
        username = message_data.get('username')

        if body:
            message.body = body
        if username:
            message.username = username

        db.session.commit()

        message_dict = message.to_dict()
        return make_response(message_dict,200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response_body={
            "delete_successful": True,
            "message": "Message Delete"
        }
        return make_response(response_body,200)


if __name__ == '__main__':
    app.run(port=5555)
