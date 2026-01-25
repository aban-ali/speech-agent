import { useEffect, useMemo, useRef, useState } from "react";
const BACKEND_URL = "http://localhost:8000";


function AgentCard({ agent, text }) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: 12,
        padding: 12,
        background: "white",
      }}
    >
      <div style={{ fontWeight: 700, marginBottom: 6 }}>
        {agent.toUpperCase()}
      </div>
      <div style={{ color: "#222" }}>{text}</div>
    </div>
  );
}

function ModeToggle({ mode, setMode }) {
  return (
    <>
    <hr />
    <div className="modeToggle">
        <h4>Choose Model Mode:</h4>
        <button
            className={`modeBtn ${mode === "local" ? "active" : ""}`}
            onClick={() => setMode("local")}
            type="button"
          >
            Local Model
        </button>

        <button
            className={`modeBtn ${mode === "grok" ? "active" : ""}`}
            onClick={() => setMode("grok")}
            type="button"
        >
            Grok (Proprietary)
        </button>
    </div>
    </>
  );
}



export function Agent() {
  const [supported, setSupported] = useState(true);
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("grok");


  const [transcript, setTranscript] = useState("");
  const [agents, setAgents] = useState([]);
  const [finalAudioUrl, setFinalAudioUrl] = useState("");

  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const streamRef = useRef(null);

  const canRecord = useMemo(() => {
    return (
      typeof window !== "undefined" &&
      !!navigator.mediaDevices?.getUserMedia &&
      !!window.MediaRecorder
    );
  }, []);

  useEffect(() => {
    setSupported(canRecord);
  }, [canRecord]);

  async function startRecording() {
    if (!canRecord) {
      alert("Recording not supported in this browser.");
      return;
    }

    setTranscript("");
    setAgents([]);
    setFinalAudioUrl("");

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    streamRef.current = stream;

    chunksRef.current = [];

    const recorder = new MediaRecorder(stream, {
      mimeType: "audio/webm", // best supported
    });

    recorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) chunksRef.current.push(e.data);
    };

    recorder.onstop = async () => {
      const blob = new Blob(chunksRef.current, { type: "audio/webm" });
      await sendAudioToBackend(blob);

      // cleanup mic
      streamRef.current?.getTracks()?.forEach((t) => t.stop());
      streamRef.current = null;
    };

    mediaRecorderRef.current = recorder;
    recorder.start();
    setRecording(true);
  }

  function stopRecording() {
    if (!mediaRecorderRef.current) return;
    mediaRecorderRef.current.stop();
    setRecording(false);
  }

  async function sendAudioToBackend(blob) {
    setLoading(true);

    try {
      const form = new FormData();
      form.append("file", blob, "recording.webm");
      form.append("mode", mode);

      const res = await fetch(`${BACKEND_URL}/run`, {
        method: "POST",
        body: form,
      });
      console.log("Response received from backend");
      if (!res.ok) throw new Error("Backend error");
      console.log("Response OK");
      const data = await res.json();
      console.log("Response JSON parsed", data);
      setTranscript(data.transcript || "");
      setAgents(data.agents || []);

      if (data.output_audio) {
        // cache bust so browser reloads new audio
        setFinalAudioUrl(
          `${BACKEND_URL}${data.output_audio}?t=${Date.now()}`
        );
      }
    } catch (err) {
      console.error(err);
      alert("Failed. Check backend logs + CORS.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
    <ModeToggle mode={mode} setMode={setMode} />
    {!supported && (
        <div
          style={{
            padding: 12,
            borderRadius: 12,
            background: "#fff3cd",
            border: "1px solid #ffeeba",
            marginBottom: 16,
          }}
        >
          Your browser doesn't support audio recording. Try Chrome.
        </div>
      )}

      <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
        {!recording ? (
          <button
            onClick={startRecording}
            disabled={!supported || loading}
            style={{
              padding: "10px 14px",
              borderRadius: 10,
              border: "1px solid #ddd",
              cursor: "pointer",
            }}
          >
            🎙 Start Recording
          </button>
        ) : (
          <button
            onClick={stopRecording}
            style={{
              padding: "10px 14px",
              borderRadius: 10,
              border: "1px solid #ddd",
              cursor: "pointer",
            }}
          >
            ⏹ Stop
          </button>
        )}

        {loading && <span style={{ color: "#666" }}>Running…</span>}
      </div>

      <hr style={{ margin: "20px 0" }} />

      <h2 style={{ marginBottom: 8 }}>Transcript</h2>
      <textarea
        value={transcript}
        readOnly
        rows={4}
        placeholder="Transcript will appear here..."
        style={{
          width: "90%",
          padding: 12,
          borderRadius: 12,
          border: "1px solid #ddd",
          resize: "none",
        }}
      />

      <h2 style={{ marginTop: 20, marginBottom: 10 }}>Agents</h2>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        {agents.length === 0 ? (
          <div style={{ color: "#666" }}>
            Agent responses will appear here.
          </div>
        ) : (
          agents.map((a) => (
            <AgentCard key={a.agent} agent={a.agent} text={a.text} />
          ))
        )}
      </div>

      <h2 style={{ marginTop: 20, marginBottom: 10 }}>Final Audio</h2>
      {finalAudioUrl ? (
        <audio controls src={finalAudioUrl} style={{ width: "100%" }} />
      ) : (
        <div style={{ color: "#666" }}>Mixed audio will appear here.</div>
      )}
    </>
  );
}