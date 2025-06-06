#!/usr/bin/env python3
"""
Simple Flask app to test Ollama integration
"""
import os
import requests
import json
from flask import Flask, render_template_string, request, jsonify
import time

app = Flask(__name__)

# Configuration
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama:11434')
DEFAULT_MODEL = 'llama3.2:3b'

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🤖 Ollama Test App</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 20px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
            color: white; 
            padding: 30px; 
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .status { 
            padding: 20px; 
            text-align: center; 
            border-bottom: 1px solid #eee;
        }
        .status.online { background: #d4edda; color: #155724; }
        .status.offline { background: #f8d7da; color: #721c24; }
        .chat-area { 
            height: 400px; 
            overflow-y: auto; 
            padding: 20px; 
            background: #f8f9fa;
        }
        .message { 
            margin: 15px 0; 
            padding: 15px; 
            border-radius: 15px; 
            max-width: 80%;
        }
        .user { 
            background: #007bff; 
            color: white; 
            margin-left: auto; 
            text-align: right;
        }
        .ai { 
            background: white; 
            border: 1px solid #dee2e6;
            margin-right: auto;
        }
        .input-area { 
            padding: 20px; 
            display: flex; 
            gap: 10px;
            background: white;
        }
        #messageInput { 
            flex: 1; 
            padding: 15px; 
            border: 2px solid #dee2e6; 
            border-radius: 25px; 
            font-size: 16px;
            outline: none;
        }
        #messageInput:focus { border-color: #007bff; }
        #sendBtn { 
            padding: 15px 30px; 
            background: #007bff; 
            color: white; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer; 
            font-weight: bold;
            transition: all 0.3s;
        }
        #sendBtn:hover { background: #0056b3; transform: translateY(-2px); }
        #sendBtn:disabled { background: #6c757d; cursor: not-allowed; transform: none; }
        .model-selector { 
            padding: 20px; 
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }
        select { 
            padding: 10px; 
            border: 1px solid #dee2e6; 
            border-radius: 10px; 
            font-size: 14px;
        }
        .loading { opacity: 0.7; }
        .metrics { 
            padding: 10px 20px; 
            background: #e9ecef; 
            font-size: 12px; 
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Ollama Test App</h1>
            <p>Multi-container Docker deployment test</p>
        </div>
        
        <div id="status" class="status">
            <span id="statusText">🔄 Checking connection...</span>
        </div>
        
        <div class="model-selector">
            <label>Model: </label>
            <select id="modelSelect">
                <option value="llama3.2:3b">Llama 3.2 3B</option>
                <option value="phi3:mini">Phi-3 Mini</option>
            </select>
            <span id="modelInfo" style="margin-left: 20px; font-size: 12px; color: #6c757d;"></span>
        </div>
        
        <div id="chatArea" class="chat-area">
            <div class="message ai">
                <strong>🤖 Assistant:</strong> Hello! I'm running in a separate Docker container from Ollama. Try asking me something!
            </div>
        </div>
        
        <div class="metrics" id="metrics">
            Response time: -- | Tokens: -- | Container: test-app → ollama-server
        </div>
        
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Type your message..." 
                   onkeypress="handleKeyPress(event)">
            <button id="sendBtn" onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        let isOnline = false;
        
        // Check Ollama status on page load
        checkStatus();
        
        async function checkStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                isOnline = data.online;
                
                const statusEl = document.getElementById('status');
                const statusText = document.getElementById('statusText');
                
                if (isOnline) {
                    statusEl.className = 'status online';
                    statusText.textContent = `✅ Connected to Ollama (${data.version})`;
                } else {
                    statusEl.className = 'status offline';
                    statusText.textContent = '❌ Ollama not available';
                }
            } catch (error) {
                console.error('Status check failed:', error);
            }
        }
        
        async function sendMessage() {
            if (!isOnline) {
                alert('Ollama is not available');
                return;
            }
            
            const input = document.getElementById('messageInput');
            const chatArea = document.getElementById('chatArea');
            const sendBtn = document.getElementById('sendBtn');
            const modelSelect = document.getElementById('modelSelect');
            const metrics = document.getElementById('metrics');
            
            const message = input.value.trim();
            if (!message) return;
            
            // Add user message
            chatArea.innerHTML += `
                <div class="message user">
                    <strong>You:</strong> ${message}
                </div>
            `;
            
            input.value = '';
            sendBtn.disabled = true;
            sendBtn.textContent = 'Thinking...';
            
            const startTime = Date.now();
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        model: modelSelect.value
                    })
                });
                
                const data = await response.json();
                const endTime = Date.now();
                const responseTime = ((endTime - startTime) / 1000).toFixed(1);
                
                if (data.success) {
                    chatArea.innerHTML += `
                        <div class="message ai">
                            <strong>🤖 Assistant:</strong> ${data.response}
                        </div>
                    `;
                    
                    // Update metrics
                    const tokenCount = data.response.split(' ').length;
                    metrics.textContent = `Response time: ${responseTime}s | Tokens: ~${tokenCount} | Model: ${modelSelect.value}`;
                } else {
                    chatArea.innerHTML += `
                        <div class="message ai">
                            <strong>❌ Error:</strong> ${data.error}
                        </div>
                    `;
                }
            } catch (error) {
                chatArea.innerHTML += `
                    <div class="message ai">
                        <strong>❌ Error:</strong> ${error.message}
                    </div>
                `;
            }
            
            sendBtn.disabled = false;
            sendBtn.textContent = 'Send';
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Auto-refresh status every 30 seconds
        setInterval(checkStatus, 30000);
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "ollama-test-app"})

@app.route('/api/status')
def status():
    try:
        response = requests.get(f'{OLLAMA_URL}/api/version', timeout=5)
        if response.status_code == 200:
            version_data = response.json()
            return jsonify({
                "online": True,
                "version": version_data.get("version", "unknown"),
                "ollama_url": OLLAMA_URL
            })
    except Exception as e:
        print(f"Status check failed: {e}")
    
    return jsonify({"online": False, "error": "Cannot connect to Ollama"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        model = data.get('model', DEFAULT_MODEL)
        
        if not message:
            return jsonify({"success": False, "error": "No message provided"})
        
        # Call Ollama API
        ollama_response = requests.post(
            f'{OLLAMA_URL}/api/generate',
            json={
                "model": model,
                "prompt": message,
                "stream": False
            },
            timeout=60
        )
        
        if ollama_response.status_code == 200:
            result = ollama_response.json()
            return jsonify({
                "success": True,
                "response": result.get('response', 'No response'),
                "model": model
            })
        else:
            return jsonify({
                "success": False,
                "error": f"Ollama API error: {ollama_response.status_code}"
            })
            
    except requests.Timeout:
        return jsonify({"success": False, "error": "Request timeout"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/models')
def models():
    try:
        response = requests.get(f'{OLLAMA_URL}/api/tags', timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Models fetch failed: {e}")
    
    return jsonify({"models": []})

if __name__ == '__main__':
    print("🚀 Starting Ollama Test App...")
    print(f"📡 Ollama URL: {OLLAMA_URL}")
    print("🌐 Web interface will be available at http://localhost:8080")
    
    # Wait for Ollama to be ready
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(f'{OLLAMA_URL}/api/version', timeout=2)
            if response.status_code == 200:
                print("✅ Ollama is ready!")
                break
        except:
            if i < max_retries - 1:
                print(f"⏳ Waiting for Ollama... ({i+1}/{max_retries})")
                time.sleep(2)
            else:
                print("⚠️  Starting without Ollama connection")
    
    app.run(host='0.0.0.0', port=8080, debug=False)