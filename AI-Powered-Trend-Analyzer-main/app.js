document.getElementById("sendButton").addEventListener("click", sendMessage);
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {
    const inputBox = document.getElementById("userInput");
    const userText = inputBox.value.trim();
    
    if (userText) {
        // Display user message
        displayMessage(userText, "user-message");
        inputBox.value = "";

        // Mock AI response (replace this with actual API call to get response)
        setTimeout(() => {
            const botResponse = generateBotResponse(userText);
            displayMessage(botResponse, "bot-message");
        }, 1000);
    }
}

function displayMessage(text, className) {
    const chatBox = document.getElementById("chatBox");
    const message = document.createElement("div");
    message.classList.add("message", className);
    message.innerText = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function generateBotResponse(userText) {
    // Simple response logic for demo purposes
    return `You said: ${userText}`;
}
