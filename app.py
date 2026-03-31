from flask import Flask, request, jsonify, render_template_string
import requests
from PyPDF2 import PdfReader

app = Flask(__name__)

pdf_path = "Zengtao_Liang_Resume.pdf"

try:
    reader = PdfReader(pdf_path)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() + "\n"
    print("PDF loaded successfully.")
except Exception as e:
    print("Error reading PDF:", e)
    resume_text = "Resume text could not be loaded."


@app.route("/", methods=["GET"])
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>RESUME_BOT.SYS</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

            :root {
                --pink-primary: #ec4899;
                --pink-light: #ffe4e6;
                --bg-gradient: linear-gradient(135deg, #fff1f5 0%, #ffe4e6 100%);
            }

            body { 
                background: var(--bg-gradient); 
                color: #000; 
                font-family: 'Press Start 2P', cursive; 
                display: flex; 
                flex-direction: column; 
                align-items: center; 
                padding: 20px; 
                min-height: 100vh;
                margin: 0;
                image-rendering: pixelated;
            }

            h2 { 
                color: black; 
                text-shadow: 2px 2px var(--pink-primary);
                font-size: 16px;
                margin-top: 40px;
                letter-spacing: 1px;
            }


            #chat-box { 
                background: white; 
                border: 4px solid black; 
                box-shadow: 8px 8px 0px 0px rgba(0,0,0,1);
                width: 95%; 
                max-width: 650px; 
                height: 450px; 
                overflow-y: auto; 
                padding: 20px; 
                display: flex; 
                flex-direction: column; 
                gap: 15px; 
                margin-bottom: 20px;
                box-sizing: border-box;
            }


            .bubble { 
                padding: 12px; 
                border: 3px solid black;
                max-width: 80%; 
                word-wrap: break-word; 
                font-size: 9px;
                line-height: 1.6;
                position: relative;
            }


            .user { 
                background: var(--pink-primary); 
                color: white; 
                align-self: flex-end; 
                box-shadow: 4px 4px 0px 0px black;
            }


            .model { 
                background: #f3f4f6; 
                color: black; 
                align-self: flex-start; 
                box-shadow: -4px 4px 0px 0px black;
            }


            @keyframes pixel-flash {
                0%, 100% { opacity: 1; transform: scale(1); }
                50% { opacity: 0.5; transform: scale(0.98); }
            }

            .thinking {
                background: white !important;
                border: 3px dashed var(--pink-primary) !important;
                color: var(--pink-primary) !important;
                animation: pixel-flash 0.8s infinite;
                font-size: 8px !important;
            }


            #input-area { 
                display: flex; 
                width: 95%; 
                max-width: 650px; 
                gap: 10px; 
            }

            #input-area input { 
                flex: 1; 
                padding: 12px; 
                font-family: 'Press Start 2P', cursive;
                font-size: 10px; 
                border: 4px solid black; 
                background: white; 
                outline: none;
            }

            #input-area button { 
                padding: 12px 20px; 
                font-family: 'Press Start 2P', cursive;
                font-size: 10px; 
                border: 4px solid black; 
                background: var(--pink-primary); 
                color: white; 
                cursor: pointer; 
                box-shadow: 4px 4px 0px 0px black;
                transition: transform 0.05s;
            }

            #input-area button:active { 
                transform: translate(2px, 2px);
                box-shadow: 2px 2px 0px 0px black;
            }


            #chat-box::-webkit-scrollbar { width: 14px; }
            #chat-box::-webkit-scrollbar-track { background: var(--pink-light); border-left: 3px solid black; }
            #chat-box::-webkit-scrollbar-thumb { background: black; border: 2px solid white; }
        </style>
    </head>
    <body>
        <h2>TALK TO MY RESUME BOT</h2>
        <div id="chat-box"></div>
        <div id="input-area">
            <input id="input" placeholder="ASK ABOUT PROJECTS..." autocomplete="off" />
            <button onclick="send()">SEND</button>
        </div>

        <script>
        async function send() {
            const inputEl = document.getElementById("input");
            const chatBox = document.getElementById("chat-box");
            const message = inputEl.value.trim();
            if (!message) return;


            const userBubble = document.createElement("div");
            userBubble.className = "bubble user";
            userBubble.textContent = message;
            chatBox.appendChild(userBubble);
            chatBox.scrollTop = chatBox.scrollHeight;
            inputEl.value = "";


            const thinkingBubble = document.createElement("div");
            thinkingBubble.className = "bubble model thinking";
            thinkingBubble.textContent = "SYSTEM_THINKING...";
            chatBox.appendChild(thinkingBubble);
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const res = await fetch("/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message})
                });
                const data = await res.json();
                
                // 3. Replace Thinking Bubble with Bot Reply
                thinkingBubble.classList.remove("thinking");
                thinkingBubble.textContent = data.reply;
            } catch (err) {
                thinkingBubble.classList.remove("thinking");
                thinkingBubble.style.color = "red";
                thinkingBubble.textContent = "SYSTEM_ERROR: OLLAMA_NOT_FOUND";
            }
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // Listen for Enter Key
        document.getElementById("input").addEventListener("keypress", (e) => {
            if(e.key === "Enter") send();
        });
        </script>
    </body>
    </html>
    """)


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]


    prompt = f"""
    Context: {resume_text}
    Task: Answer the user's question based strictly on the resume above.
    Tone: Professional, helpful, concise.
    User Question: {user_message}
    """

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:latest",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        data = response.json()
        

        reply_text = data.get("response") or "I encountered a processing error."
        return jsonify({"reply": reply_text.strip()})
    
    except Exception as e:
        print("API Error:", e)
        return jsonify({"reply": "CONNECTION_FAILED: Ensure Ollama is running locally."})

if __name__ == "__main__":
    app.run(debug=True)