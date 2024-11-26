import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv;load_dotenv()

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
            print(f"\033[1;91m{e}\033[0m")
            print(self._get_token())  # Fetch a new token
            self.__init__()  # Reinitialize after fetching the token
        except json.JSONDecodeError:
            # Handle corrupted or invalid JSON file
            print("\033[1;91mError: Your JSON file is corrupted or does not match the required credentials format. Please reinitialize or regenerate the file.\033[0m")
            print(self._get_token())  # Fetch a new token
            self.__init__()  # Reinitialize after fetching the token
        except KeyError as e:
            # Handle missing keys in the JSON file
            print(f"\033[1;91mError: Missing required key {e} in the JSON file. Please reinitialize or regenerate the file.\033[0m")
            print(self._get_token())  # Fetch a new token
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
                return f"\033[1;92mToken saved to {self.credentials_file} successfully.\033[0m\n"
            elif response.status_code==400:
                return f"\033[1;91mError {json.loads(response.content)['error']['message']} Make Sure You have Provided the ***KEY*** and ***REFRESH_TOKEN***\033[0m\n"
            else:
                return f"\033[1;91mError {response.status_code}: {response.content}\033[0m\n"
        except requests.exceptions.RequestException as e:
            return f"\033[1;91mRequest failed: {str(e)}\033[0m\n"

    def chat(self, query: str, stream: bool = True) -> str:
        """
        ## Sends a chat message to the IraAI API and returns the response.

        - Args:
            - query (str): The user's message to send to the chatbot.
            - stream (bool): Whether to print the response in real-time (default: True).

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

        # Payload for the API request
        json_data = {
            'firebaseId': self.firebaseId,
            'messages': [
                {
                    'content': query,
                    'role': 'user',
                    'timestamp': timestamp,
                    'reactions': {'like': True, 'love': True, 'haha': True},
                    'showReactions': True,
                    'status': 'sent',
                    'type': 'text_message',
                },
            ],
            'chemistryId': 1,
        }
        try:
            # Send the chat request
            response = requests.post(
                'https://rumik-ai.onrender.com/v1/users/messages',
                headers=headers,
                json=json_data,
                stream=stream,
                timeout=100  # Set a timeout for the request
            )

            if response.status_code == 200:
                # Process the streaming response
                streaming_response = ''
                data = response.json()
                for message in data:
                    stream_data = f"{message['content']} "
                    if stream:
                        print(stream_data, end="", flush=True)
                    streaming_response += stream_data
                return streaming_response
            elif response.status_code == 403:
                return "\033[1;91mToken expired. Generating a new one...\033[0m"
            else:
                return f"Error {response.status_code}: {response.content}"
        except requests.exceptions.RequestException as e:
            return f"\033[1;91mRequest failed: {str(e)}\033[0m"

if __name__ == "__main__":
    AI = IraAI()
    while True:
        query = input("You: ")
        if not query.strip():continue
        print(f"\nIraAI: \033[1;93m{AI.chat(query=query.strip(), stream=False)}\033[0m\n")
