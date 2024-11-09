let currentSessionId = null;

document.getElementById("sendButton").addEventListener("click", sendMessage);
document.getElementById("historyButton").addEventListener("click", toggleHistory);
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {
    const inputBox = document.getElementById("userInput");
    const userText = inputBox.value.trim();
    
    if (userText) {
        displayMessage(userText, "user-message");
        inputBox.value = "";

        try {
            const response = await fetch("http://127.0.0.1:8000/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: userText, session_id: currentSessionId })
            });

            if (response.ok) {
                const data = await response.json();
                currentSessionId = data.session_id;
                displayMessage(data.response, "bot-message");
            } else {
                displayMessage("Error: Unable to get response from server.", "bot-message");
            }
        } catch (error) {
            displayMessage("Error: Server is unreachable.", "bot-message");
        }
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

async function toggleHistory() {
    const historyTab = document.getElementById("historyTab");
    if (historyTab.style.display === "none") {
        historyTab.style.display = "block";
        loadHistorySessions();
    } else {
        historyTab.style.display = "none";
    }
}

async function loadHistorySessions() {
    const response = await fetch("http://127.0.0.1:8000/sessions");
    const data = await response.json();
    const historyTab = document.getElementById("historyTab");

    historyTab.innerHTML = ""; // Clear previous history
    data.sessions.forEach(sessionId => {
        const sessionElement = document.createElement("div");
        sessionElement.classList.add("history-session");
        sessionElement.innerText = `Session: ${sessionId}`;
        sessionElement.onclick = () => loadSessionHistory(sessionId);
        historyTab.appendChild(sessionElement);
    });
}

async function loadSessionHistory(sessionId) {
    const response = await fetch(`http://127.0.0.1:8000/history/${sessionId}`);
    const data = await response.json();
    const chatBox = document.getElementById("chatBox");

    chatBox.innerHTML = ""; // Clear current chat
    data.history.forEach(chat => {
        displayMessage(chat.user_message, "user-message");
        displayMessage(chat.bot_response, "bot-message");
    });

    currentSessionId = sessionId;  // Set this session as current
}