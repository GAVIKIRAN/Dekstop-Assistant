// Function to update the chat container with new messages
function updateChat(message, isUser = true) {
    const chatContainer = document.getElementById('chatContainer');
    const chatEntry = document.createElement('div');
    chatEntry.classList.add('chat-entry');
    chatEntry.innerHTML = `<div class="${isUser ? 'user-message' : 'assistant-message'}">${message}</div>`;
    chatContainer.appendChild(chatEntry);
    chatContainer.scrollTop = chatContainer.scrollHeight;  // Scroll to the latest message
}

// Handle text input
function openWebsiteByText() {
    const website = document.getElementById("websiteText").value;
    updateChat(`You: ${website}`, true);

    fetch('/open_website_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'website=' + website
    })
    .then(response => response.json())
    .then(data => {
        updateChat(`Assistant: ${data.message}`, false);
    });

    document.getElementById("websiteText").value = ''; // Clear the input field
}

// Handle voice input
function openWebsiteByVoice() {
    updateChat("You: (Voice Command)", true);  // Placeholder for voice input

    fetch('/open_website_voice', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        updateChat(`Assistant: ${data.message}`, false);
    });
}
function startVirtualMouse() {
    fetch('/start_virtual_mouse', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);  // Alert the user
    });
}
