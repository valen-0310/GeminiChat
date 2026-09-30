const messagesEl = document.getElementById("messages");
const form = document.getElementById("messageForm");
const input = document.getElementById("messageInput");
const clearBtn = document.getElementById("clearBtn");
const emojiBtn = document.getElementById("emojiBtn");
const lastPreview = document.getElementById("lastPreview");
const lastTime = document.getElementById("lastTime");

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function renderMessages(messages) {
    messagesEl.innerHTML = "";

    const label = document.createElement("div");
    label.className = "day-label";
    label.textContent = "HOY";
    messagesEl.appendChild(label);

    messages.forEach(message => {
        const wrapper = document.createElement("div");
        wrapper.className = `message ${message.sender}`;

        const bubble = document.createElement("div");
        bubble.className = "bubble";

        const text = document.createElement("span");
        text.innerHTML = escapeHtml(message.text).replace(/\n/g, "<br>");
        bubble.appendChild(text);

        const meta = document.createElement("span");
        meta.className = "meta";
        meta.innerHTML = `${escapeHtml(message.time)} ${message.sender === "user" ? '<span class="check">✓✓</span>' : ""}`;
        bubble.appendChild(meta);

        wrapper.appendChild(bubble);
        messagesEl.appendChild(wrapper);
    });

    messagesEl.scrollTop = messagesEl.scrollHeight;

    if (messages.length) {
        const last = messages[messages.length - 1];
        lastPreview.textContent = last.text;
        lastTime.textContent = last.time;
    }
}

async function loadMessages() {
    const response = await fetch("/api/messages");
    const data = await response.json();
    renderMessages(data);
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = input.value.trim();
    if (!text) return;

    input.value = "";
    input.focus();

    const response = await fetch("/api/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    if (!response.ok) {
        alert("No se pudo enviar el mensaje.");
        return;
    }

    await loadMessages();
});

clearBtn.addEventListener("click", async () => {
    await fetch("/api/messages", { method: "DELETE" });
    await loadMessages();
});

emojiBtn.addEventListener("click", () => {
    input.value += "😊";
    input.focus();
});

document.getElementById("searchInput").addEventListener("input", (event) => {
    const query = event.target.value.toLowerCase();
    const item = document.querySelector(".chat-item");

    if (query && !"asistente chatbot".includes(query)) {
        item.style.display = "none";
    } else {
        item.style.display = "flex";
    }
});

loadMessages();
