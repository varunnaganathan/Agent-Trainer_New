from flask import Flask, request, jsonify
import logging
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_root():
    return jsonify({'message': 'This is a GET request response'}), 200

@app.route('/callbacks/vapi', methods=['POST'])
def post_root():
    try:
        # Parse the incoming JSON data
        data = request.json
        app.logger.info('POST request received with data: %s', json.dumps(data, indent=2))
        
        # Extract information from the JSON payload
        message = data.get('message', {})
        message_type = message.get('type', 'unknown')
        call_object = message.get('call', {})
        function_call = message.get('functionCall', {})
        function_name = function_call.get('name', 'unknown')
        parameters = function_call.get('parameters', '{}')
        
        # Log the extracted information
        app.logger.info('Message type: %s', message_type)
        app.logger.info('Call object: %s', call_object)
        app.logger.info('Function name: %s', function_name)
        app.logger.info('Parameters: %s', parameters)
        print(jsonify({'received_data2': data}))
        print("\n\n")
        print(data["message"])
        # Respond with the received data
        return jsonify({'received_data2': data}), 201
    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({'error': 'Failed to process request'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
