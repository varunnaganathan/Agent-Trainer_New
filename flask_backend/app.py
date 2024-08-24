from flask import Flask, request, jsonify
import logging
import json
import requests



app = Flask(__name__)


logging.basicConfig(level=logging.INFO)



@app.route('/', methods=['GET'])
def get_root():
    chatId = request.args.get('chatId')
    # get chat id
    #chatId = data.get('chatId')
    print(chatId)
    return jsonify({'chatId': str(chatId)}), 200

@app.route('/analyze', methods=['GET'])
def get_report():
    try:
        # get chat id
        chatId = request.args.get('chatId')
        print("chatId.  = " + str(chatId))
        logging.info(f"chatId: {chatId}")

        # call hume
        chatData = get_chat_data(chatId)
        logging.info(f"chatData final: {chatData}")
        # process data here
        print(chatData)
        return jsonify(str(chatData)), 200
    except Exception as e:
        app.logger.error('Error processing request: %s', str(e))
        return jsonify({'error':str(e)}), 400


def get_chat_data(chatId):
    # URL of the API you want to send a GET request to
    api_url = 'https://api.hume.ai/v0/evi/chats' 
    
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
        logging.info(f"response from inner func: {response}")

        # Check if the request was successful
        if response.status_code == 200:
            # Get the JSON response data
            data = response.json()
            logging.info(f"response from inner func 2 after .json call: {data}")
            return jsonify({'status': 'success', 'data': data}), 200
        else:
            # Handle errors
            return jsonify({'status': 'error', 'message': 'Failed to fetch data'}), response.status_code
    
    except requests.exceptions.RequestException as e:
        # Handle network errors
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=True)
