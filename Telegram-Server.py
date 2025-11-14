import os
import json
import random
import logging
import requests
from time import sleep
from datetime import datetime
from telegram import Update, error
from dotenv import load_dotenv;load_dotenv()
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
class IraAI:
    """
    ## A class to interact with the IraAI chatbot API. Handles token management, user authentication, and sending/receiving chat messages.

    - Attributes:
        - access_token (str): Bearer token for authenticating API requests.
        - firebaseId (str): Unique identifier for the user.
    """
    def __init__(self) -> None:
        """
        - Initializes the IraAI instance by loading or generating necessary credentials.
        - If the credentials file does not exist or is corrupted, it fetches a new token.
        """
        self.credentials_file = r'IraAI.json'  # Path to the credentials file
        try:
            # Check if the credentials file exists
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as json_file:
                    data = json.load(json_file)
                # Set attributes from the JSON data
                self.access_token = data['access_token']
                self.firebaseId = data['user_id']
            else:
                raise FileNotFoundError("Credentials File Not Found.")
        except FileNotFoundError as e:
            # Handle missing credentials file
            logging.info(e)
            logging.info(self._get_token())  # Fetch a new token
            self.__init__()  # Reinitialize after fetching the token
        except json.JSONDecodeError:
            # Handle corrupted or invalid JSON file
            logging.info("Error: Your JSON file is corrupted or does not match the required credentials format. Please reinitialize or regenerate the file.")
            logging.info(self._get_token())  # Fetch a new token
            self.__init__()  # Reinitialize after fetching the token
            
        except KeyError as e:
            # Handle missing keys in the JSON file
            logging.info(f"Error: Missing required key {e} in the JSON file. Please reinitialize or regenerate the file.")
            logging.info(self._get_token())  # Fetch a new token
            self.__init__()  # Reinitialize after fetching the token

    def _get_token(self) -> str:
        """
        ## Fetches a new access token from the secure token API and saves it to a JSON file.

        - Returns:
            - str: Success or error message based on the response.
        """
        headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://ira.rumik.ai',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }
        params = {'key': os.getenv('KEY')}
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': os.getenv('REFRESH_TOKEN'),
        }
        print(params, data)
        try:
            response = requests.post(
                'https://securetoken.googleapis.com/v1/token',
                params=params,
                headers=headers,
                data=data,
                timeout=100  # Set a timeout for the request
            )

            if response.status_code == 200:
                # Save the response content to the credentials file
                with open(self.credentials_file, 'w') as json_file:
                    json.dump(response.json(), json_file, indent=4)
                return f"Token saved to {self.credentials_file} successfully."
            elif response.status_code==400:
                return f"Error {json.loads(response.content)['error']['message']} Make Sure You have Provided the ***KEY*** and ***REFRESH_TOKEN***"
            else:
                return f"Error {response.status_code}: {response.content}"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"

    def chat(self, query: str) -> str:
        """
        ## Sends a chat message to the IraAI API and returns the response.

        - Args:
            - query (str): The user's message to send to the chatbot.

        - Returns:
            - str: The complete chatbot response.
        """
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {self.access_token}',
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://ira.rumik.ai',
            'priority': 'u=1, i',
            'referer': 'https://ira.rumik.ai/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        # Get the current UTC time formatted as ISO 8601 with milliseconds
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        random_chemistry_id = ''.join(random.choice('0123456789abcdef') for _ in range(24))

        # Payload for the API request
        json_data = {
            'chemistry_id': random_chemistry_id,
            'messages': [
                {
                    'content': 'aaj kya kar rhi ho?',
                    'emojiReaction': None,
                    'isCleared': False,
                    'parentMessageId': None,
                    'role': 'user',
                    'status': 'sent',
                    'timestamp': timestamp,
                    'type': 'text_message',
                },
            ],
            'user_timestamp_iso': timestamp,
        }
        try:
            # Send the chat request
            response = requests.post(
                'https://api-ira.rumik.ai/api/v3/data/messages',
                headers=headers,
                json=json_data,
                stream=True,
                timeout=100  # Set a timeout for the request
            )

            if response.status_code == 200:
                # Process the streaming response
                streaming_response = ''
                data = response.json()
                for message in data:
                    if message['role'] == 'assistant':
                        stream_data = f"{message['content']} "
                        streaming_response += stream_data
                return streaming_response
            elif response.status_code == 403:
                logging.info("Token expired. Generating a new one...")
                logging.info(self._get_token())
                self.__init__()
                return self.chat(query=query)
            else:
                return f"Error {response.status_code}: {response.content}"
        except requests.exceptions.RequestException as e:
            return f"Request failed: {str(e)}"
    
    # Define the command handler for /start command
    def start(self, update: Update, context: CallbackContext):
        user = update.message.from_user
        logging.info(f"User: {user.username} started the bot.")
        update.message.reply_text(f"Hello, {user.first_name}! kya chal rha hai. 🙂")

    # Define the text message handler to accept only text messages
    def text_handler(self, update: Update, context: CallbackContext):
        # Only accepts text messages
        if update.message.text:
            logging.info(f"User: {update.message.from_user.username}, Message: {update.message.text}")
            reply_message = self.chat(query=update.message.text.strip())
            update.message.reply_text(reply_message, timeout=None)
            logging.info(f"Ira Reply To: {update.message.from_user.username}, Message: {reply_message}\n")
        else:
            logging.info("Non-text message received, ignored.")

# Main function to set up the bot
def main():
    try:
        AI = IraAI()
        BOT_TOEKN = os.getenv('BOT_TOKEN')
    
        # Log to monitor bot startup
        logging.info('Starting Server...')

        updater = Updater(token=BOT_TOEKN, use_context=True)
    
        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher
    
        # Register command handlers
        dispatcher.add_handler(CommandHandler("start", AI.start))
    
        # Register the text message handler (only text messages are processed)
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, AI.text_handler))
    
        # Start the bot
        updater.start_polling()
    
        logging.info("Server is now running...")

        # ➤ Print bot username after startup
        bot_username = updater.bot.username
        print(f"You can chat now on 🤖 @{bot_username}\n")

        updater.idle()
    except (Exception, error.NetworkError) as e:
        logging.error(
            "Server failed to start due to an unexpected error.",
            extra={"details": str(e)}
        )
        logging.info("Attempting restart in 2 seconds...\n")
        sleep(2)
        main()  # Restart the main function on any exception

if __name__ == '__main__':
    main()
    