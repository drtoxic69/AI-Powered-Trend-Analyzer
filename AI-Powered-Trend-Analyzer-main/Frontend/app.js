document.getElementById("sendButton").addEventListener("click", sendMessage);
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});


function displayMessage(text, className) {
    const chatBox = document.getElementById("chatBox");
    const message = document.createElement("div");
    message.classList.add("message", className);
    message.innerText = text;
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const inputBox = document.getElementById("userInput");
    const userText = inputBox.value.trim();
    
    if (userText) {
        displayMessage(userText, "user-message");
        inputBox.value = "";

        // Send user input to backend API and display the AI response
        try {
            const response = await fetch("http://127.0.0.1:8000/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: userText })
            });

            if (response.ok) {
                const data = await response.json();
                displayMessage(data.response, "bot-message");
            } else {
                displayMessage("Error: Unable to get response from server.", "bot-message");
            }
        } catch (error) {
            displayMessage("Error: Server is unreachable.", "bot-message");
        }
    }
}
