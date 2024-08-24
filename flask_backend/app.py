from flask import Flask, request, jsonify
import logging
import json
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_root():
    return jsonify({'message': 'This is a GET request response'}), 200

@app.route('/analyze', methods=['POST'])
def post_root():
    try:
        # Parse the incoming JSON data
        data = request.json

        # get chat id
        chatId = data.get('chatId')
        # call hume
        chatData = get_chat_data(chatId)

        # process data here
        print(chatData)

        """
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
        """
    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({'error': 'Failed to process request'}), 400


def get_chat_data(chatId):
    # URL of the API you want to send a GET request to
    api_url = 'https://api.hume.ai/v0/evi/chats/' + str(chatId) 
    
    # add multiple page handler
    params = {
        'page_number': 0,  # Example parameter, replace with your actual parameters
        'page_size': 100           # Another example parameter
    }
    headers = {
        "X-Hume-Api-Key":"QAmS4Qs8QGG4fbyWRG8L8xIvbZDRL6CXRuF0lE2AdQ1jtfqQ"
    }
    

    try:
        # Send the GET request
        response = requests.get(api_url, params=params, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Get the JSON response data
            data = response.json()
            return jsonify({'status': 'success', 'data': data}), 200
        else:
            # Handle errors
            return jsonify({'status': 'error', 'message': 'Failed to fetch data'}), response.status_code
    
    except requests.exceptions.RequestException as e:
        # Handle network errors
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
