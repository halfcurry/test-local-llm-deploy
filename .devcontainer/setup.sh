#!/bin/bash

# .devcontainer/setup.sh
echo "🚀 Setting up Ollama in GitHub Codespaces..."

# Wait for Ollama service to be ready
echo "⏳ Waiting for Ollama service..."
sleep 10

# With 16GB RAM, you can run much better models!
echo "📥 Pulling optimized models for 16GB RAM..."

# Primary recommendation: Llama 3.2 3B (excellent quality, fits well in 16GB)
echo "🦙 Pulling Llama 3.2 3B - High quality, perfect for 16GB..."
ollama pull llama3.2:3b

# Alternative: Qwen2.5 7B (if you want even better quality)
echo "🚀 Pulling Qwen2.5 7B - Premium model, uses ~10-12GB RAM..."
ollama pull qwen2.5:7b

# Backup smaller model for comparison
echo "⚡ Pulling Phi-3 Mini as backup (3.8GB)..."
ollama pull phi3:mini

echo "💾 Storage usage after model downloads:"
du -sh ~/.ollama/

# Create a simple test script
cat > test_model.py << 'EOF'
#!/usr/bin/env python3
import requests
import json

def test_ollama():
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.2:3b",  # Using the better model for 16GB RAM
        "prompt": "Write a detailed explanation of how large language models work:",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        print("🤖 AI Response:")
        print(result['response'])
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ollama()
EOF

chmod +x test_model.py

# Install required Python packages
pip install requests

# Create a simple web interface
cat > simple_chat.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Ollama Chat</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        #chat { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        #input { width: 70%; padding: 10px; }
        #send { padding: 10px 20px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background-color: #e3f2fd; }
        .ai { background-color: #f3e5f5; }
    </style>
</head>
<body>
    <h1>🤖 Ollama Chat Interface</h1>
    <div id="chat"></div>
    <div>
        <input type="text" id="input" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
        <button id="send" onclick="sendMessage()">Send</button>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('input');
            const chat = document.getElementById('chat');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            chat.innerHTML += `<div class="message user"><strong>You:</strong> ${message}</div>`;
            input.value = '';
            
            try {
                const response = await fetch('http://localhost:11434/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        model: 'llama3.2:3b',  // Better model for your 16GB setup
                        prompt: message,
                        stream: false
                    })
                });
                
                const data = await response.json();
                chat.innerHTML += `<div class="message ai"><strong>AI:</strong> ${data.response}</div>`;
            } catch (error) {
                chat.innerHTML += `<div class="message ai"><strong>Error:</strong> ${error.message}</div>`;
            }
            
            chat.scrollTop = chat.scrollTop + 1000;
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>
EOF

# Start a simple HTTP server for the web interface
python3 -m http.server 8080 &

echo "✅ Setup complete!"
echo "🔗 Ollama API: http://localhost:11434"
echo "🌐 Web Interface: http://localhost:8080/simple_chat.html"
echo "🧪 Test with: python3 test_model.py"
echo ""
echo "📋 Available commands:"
echo "  ollama list                    # Show installed models"
echo "  ollama run llama3.2:3b        # Chat with main model"
echo "  ollama run qwen2.5:7b         # Chat with premium model"
echo "  ollama run phi3:mini          # Chat with fast model"
echo "  ollama pull <model>           # Download new models"
echo ""
echo "🎯 Model recommendations for 16GB RAM:"
echo "  • llama3.2:3b    - Best balance (2GB model, ~6GB RAM usage)"
echo "  • qwen2.5:7b     - Highest quality (~10GB RAM usage)"
echo "  • codellama:7b   - Best for coding (~10GB RAM usage)"
echo "  • mixtral:8x7b   - Expert model (~26GB, might be tight)"