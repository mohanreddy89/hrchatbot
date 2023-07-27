from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

# A simple dictionary to store responses for different keywords
responses = {
    "payroll": "Your payroll is processed on a monthly basis.",
    "salary slips": "You can access your salary slips through our employee portal.",
    "attendance logs": "We maintain attendance logs using our biometric system.",
    "employee status": "To check your employee status, please provide your employee ID.",
    "expenses": "You can submit your expense report to the finance department.",
}

def find_response(user_input):
    for keyword, response in responses.items():
        if re.search(rf"\b{keyword}\b", user_input, re.IGNORECASE):
            return response
    return "I'm sorry, I don't have information on that topic."

index_template = """
<!DOCTYPE html>
<html>
<head>
    <title>HR Chatbot</title>
</head>
<body>
    <h1>Welcome to HR Chatbot</h1>
    <div id="chat-container">
        <div id="chat-display"></div>
        <div id="user-input">
            <input type="text" id="user-input-box" placeholder="Ask your question here..." autofocus>
            <button id="send-button">Send</button>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const chatDisplay = document.getElementById('chat-display');
            const userInputElement = document.getElementById('user-input-box');
            const sendButton = document.getElementById('send-button');

            function addMessageToChat(message, sender) {
                const messageElement = document.createElement('div');
                messageElement.innerHTML = `<strong>${sender}: </strong>${message}`;
                chatDisplay.appendChild(messageElement);
            }

            function sendMessage() {
                const userInput = userInputElement.value.trim();
                if (userInput !== '') {
                    addMessageToChat(userInput, 'You');
                    userInputElement.value = '';
                    fetch('/chatbot', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: `user_input=${encodeURIComponent(userInput)}`
                    })
                    .then(response => response.json())
                    .then(data => {
                        addMessageToChat(data.response, 'HR Bot');
                    })
                    .catch(error => {
                        console.error('Error sending message:', error);
                    });
                }
            }

            sendButton.addEventListener('click', sendMessage);
            userInputElement.addEventListener('keydown', function(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            });

            userInputElement.focus();
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(index_template)

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_input = request.form["user_input"]
    response = find_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)