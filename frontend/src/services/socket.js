import { io } from "socket.io-client";

const socket = io("http://localhost:8000", {
  transports: ["websocket"],
});


socket.on("connect", () => {
  console.log("✅ Connected to backend:", socket.id);
});

export default socket;