const socket = io();
const message = document.getElementById("message");
const messages = document.getElementById("messages");
const send = document.getElementById("send");

socket.on("connect", () => {
  socket.emit("join", { room_id: message.dataset.roomid });
});

socket.on("message", (data) => {
  const userid = message.dataset.userid
  const messageContainer = document.createElement("div");
  const messageDiv = document.createElement('div')
  if (data.sender_id === userid) {
    messageContainer.className = 'chat chat-end'
    messageDiv.className = 'chat-bubble chat-bubble-info'
  } else {
    messageContainer.className = 'chat chat-start'
    messageDiv.className = 'chat-bubble'
  }
  messageDiv.innerHTML = data.message
  messageContainer.appendChild(messageDiv)
  messages.appendChild(messageContainer);
});

send.onclick = () => {
  if (message.value != "") {
    const userid = message.dataset.userid
    socket.emit("message", {
      room_id: message.dataset.roomid,
      message: message.value,
      sender_id: userid
    });
    message.value = "";
  }
};

message.addEventListener("keyup", (event) => {
  if (event.keyCode === 13) {
    // Cancel the default action, if needed
    event.preventDefault();
    // Trigger the button element with a click
    send.click();
  }
});
