import os
from flask import Flask, request
from twilio.rest import Client
import openai
openai.api_type = "azure"
openai.api_base = "https://imaginate-azure-openai.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = "1bc3568d641a4ce1bf026974d9be2960"

app = Flask(__name__)
client = Client("AC42d87e8d49be32aec0a76539dba8839a", "ac5f599fd1235a4df132e93496484b32")
#+14155238886
messages = [{'role': 'system', 'content': 'You are a friendly assistant.'}]

def chat_completion(prompt: str) -> dict:
    '''Call Openai API for text completion
    Parameters:
        - prompt: user query (str)
    Returns:
        - dict
    '''
    messages.append({'role': 'user', 'content': prompt})
    try:
        response = openai.ChatCompletion.create(
            engine="TurboChat",
            messages=messages

        )
        reply = response['choices'][0]['message']['content']
        messages.append({"role": "assistant", "content": reply})
        return {
            'status': 1,
            'response': reply
        }
    except:
        return {
            'status': 0,
            'response': ''
        }


def send_message(to: str, message: str) -> None:
    '''
    Send message to a Whatsapp user.
    Parameters:
        - to(str): sender whatsapp number in this whatsapp:+919558515995 form
        - message(str): text message to send
    Returns:
        - None
    '''

    _ = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=to
    )


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        # Extract incoming parameters from Twilio
        message = request.form['Body']
        sender_id = request.form['From']

        # Get response from Openai
        result = chat_completion(message)
        if result['status'] == 1:
            send_message(sender_id, result['response'])
    except:
        pass
    return 'OK', 200