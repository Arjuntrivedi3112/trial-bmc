document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#chat-form');
    const input = document.querySelector('#user-input');
    const messages = document.querySelector('#messages');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const userMessage = input.value;
        input.value = '';

        if (!userMessage.trim()) return;

        messages.innerHTML += `<p>User: ${userMessage}</p>`;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            messages.innerHTML += `<p>AI: ${data.reply}</p>`;
        } catch (error) {
            console.error('Error communicating with the server:',
