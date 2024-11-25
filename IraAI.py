import requests
from datetime import datetime

class IraAI: 
    """
    A class to interact with the IraAI service.

    # Attributes
        access_token (str): The access token required to authenticate with the IraAI service.
        firebaseId (str): The unique identifier for the user in the Firebase system.

    # Methods
        __init__(access_token: str, firebaseId: str) -> None:
            Initializes the IraAI instance with the provided access token and Firebase ID.
    """
    def __init__(self, access_token: str, firebaseId: str) -> None:
        """
        Initializes the IraAI instance.

        # Args
            access_token (str): The access token required for authentication.
            firebaseId (str): The unique Firebase ID associated with the user.

        # Returns
            None
        """
        self.access_token = access_token
        self.firebaseId = firebaseId

    def chat(self, query: str, stream: bool = True) -> str:
        """
        Sends a chat message to the IraAI API and returns the response.

        Args:
            query (str): The user's message to send to the chatbot.
            stream (bool): Whether to print the response in real-time (default: True).

        Returns:
            str: The complete chatbot response.
        """
        access_token = str(self.access_token).removeprefix("Bearer ").strip()
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Bearer {access_token}',
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
                return "\033[1;91mToken expired.\033[0m"
            else:
                return f"Error {response.status_code}: {response.content}"
        except requests.exceptions.RequestException as e:
            return f"\033[1;91mRequest failed: {str(e)}\033[0m"

if __name__ == "__main__":
    AI = IraAI(access_token="Bearer eyJ......Q", firebaseId="An....3")
    while True:
        query = input("You: ")
        if not query.strip():continue
        print(f"\nIraAI: \033[1;93m{AI.chat(query=query.strip(), stream=False)}\033[0m\n")
