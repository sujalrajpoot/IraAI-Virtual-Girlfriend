# RumikaAI Virtual Girlfriend
**RumikaAI** is a Python-based virtual AI girlfriend designed for fun, casual conversations, and engaging interactions. With this program, you can chat with an AI-powered virtual personality and receive dynamic responses to your messages.

## Features
- Chat with RumikaAI using natural language.
- Real-time streaming responses for a smooth conversation experience.
- AI reactions including "like," "love," and "haha."
- Customizable for different use cases by integrating your own access tokens and Firebase IDs.

## How It Works
RumikaAI interacts with an API to simulate a virtual girlfriend experience. You provide your **access token** and **Firebase ID**, and the program sends your queries to the API to receive responses.

## Prerequisites
Before you start, ensure you have:
- Python 3.8 or later installed on your system.
- The `requests` library installed. You can install it using:
```bash
pip install requests
```
- Your personal access token and Firebase ID for authentication.

## Installation
- Clone or download the repository.
- Ensure all dependencies are installed.

## Getting Your Access Token and Firebase ID

To use the RumikaAI class, you'll need your **access_token** and **Firebase ID**. Follow the steps below to retrieve them:
```
1. Log in to your account on the RumikaAI platform.
2. Open the browser's developer tools (`F12` or `Ctrl+Shift+I` on most browsers).
3. Navigate to the **Network** tab.
4. Look for API requests (messages) containing the `Authorization` header for your `access_token`.
5. Copy the `Firebase ID` from the request payload.
```

Refer to the image below for detailed instructions:

![How to Get Access Token](access_token.png)
![How to Get Firebase ID](Firebase_ID.png)

## Usage
- Start chatting with RumikaAI:

```python
if __name__ == "__main__":
  access_token = "your_access_token_here"
  firebaseId = "your_firebase_id_here"
  rumika = RumikaAI(access_token, firebaseId)
  response = rumika.chat("Hello, Rumika!")
  print(response)
```

## Error Handling
The program includes robust error handling:

- If the access token is invalid or expired, you'll see a clear error message:
  - Token expired.
- If the request fails, the error will be displayed:
  - Request failed: Connection timed out.

## Notes
- Ensure your access token is valid to avoid authentication errors.
- API response time depends on your network speed and server availability.
- This project is designed for entertainment purposes.

## License
- This project is open-source and available under the MIT License. Feel free to modify and enhance it as you like.

## Acknowledgments
- Special thanks to the RumikaAI API service for providing the backend support for this project.

## Disclaimer
- This project is created solely for educational purposes and is not intended to disrespect or misuse the intellectual property of the creators or owners of the RumikaAI service.

- The use of this project should comply with all relevant laws and the terms and conditions of the RumikaAI platform.

- This project is intended to demonstrate the integration of AI-based conversational systems and is not for commercial or malicious use.

## Contributions Welcome
- This is an open-source project, and anyone is encouraged to contribute to improve its functionality, enhance features, or fix any issues. Please feel free to submit pull requests or report bugs to help make this project better for everyone!

# Have fun chatting with your virtual girlfriend! 💖
