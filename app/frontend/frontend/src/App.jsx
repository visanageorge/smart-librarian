import { useState, useRef } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [playingIndex, setPlayingIndex] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const audioRef = useRef(null);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMsg = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    try {
      const res = await fetch(`${API_BASE}/chat?query=${encodeURIComponent(text)}`, {
        method: "POST",
      });

      const data = await res.json();
      const botText = data.response || data.error;

      let imgUrl = null;

      // 🔥 generează imagine DOAR dacă userul cere
      if (text.toLowerCase().includes("poza") || text.toLowerCase().includes("imagine") || text.toLowerCase().includes("picture")) {
        try {
          const imgRes = await fetch(`${API_BASE}/image?prompt=${encodeURIComponent("Book cover illustration: " + botText)}`, {
            method: "POST",
          });

          if (imgRes.ok) {
            const blob = await imgRes.blob();
            imgUrl = URL.createObjectURL(blob);
          }
        } catch (e) {
          console.log("Image failed, but continuing...");
        }
      }

      const botMsg = {
        role: "assistant",
        content: botText,
        image: imgUrl,
      };

      setMessages((prev) => [...prev, botMsg]);

    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Eroare la server." },
      ]);
    }
  };

  const toggleTTS = async (text, index) => {
    if (playingIndex === index && audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
      setPlayingIndex(null);
      return;
    }

    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }

    const res = await fetch(`${API_BASE}/tts?text=${encodeURIComponent(text)}`, {
      method: "POST",
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);

    const audio = new Audio(url);
    audioRef.current = audio;
    setPlayingIndex(index);

    audio.onended = () => {
      setPlayingIndex(null);
      URL.revokeObjectURL(url);
    };

    audio.play();
  };

  const toggleRecording = async () => {
    if (isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);

    mediaRecorderRef.current = mediaRecorder;
    audioChunksRef.current = [];

    mediaRecorder.ondataavailable = (e) => {
      audioChunksRef.current.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      const blob = new Blob(audioChunksRef.current, { type: "audio/webm" });

      const formData = new FormData();
      formData.append("file", blob, "audio.webm");

      const res = await fetch(`${API_BASE}/stt`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (data.text) {
        sendMessage(data.text);
      }
    };

    mediaRecorder.start();
    setIsRecording(true);
  };

  return (
    <div className="container">
      <h1>📚 Smart Librarian</h1>

      <div className="chat">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role}>
            <div>{msg.content}</div>

            {msg.image && (
              <img src={msg.image} style={{ width: "200px", marginTop: "10px" }} />
            )}

            {msg.role === "assistant" && (
              <button onClick={() => toggleTTS(msg.content, i)}>
                {playingIndex === i ? "⏹ Stop" : "🔊 Play"}
              </button>
            )}
          </div>
        ))}
      </div>

      <div className="input-bar">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Scrie mesaj..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
        />

        <button onClick={toggleRecording}>
          {isRecording ? "🛑" : "🎤"}
        </button>

        <button onClick={() => sendMessage(input)}>➡️</button>
      </div>
    </div>
  );
}