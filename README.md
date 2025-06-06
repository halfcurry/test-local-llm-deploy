# test-local-llm-deploy

Testing Local LLM Deployment

## Installing Ollama 

```
curl -fsSL https://ollama.com/install.sh | sh

>>> Installing ollama to /usr/local
>>> Downloading Linux amd64 bundle
######################################################################## 100.0%
>>> Creating ollama user...
>>> Adding ollama user to video group...
>>> Adding current user to ollama group...
>>> Creating ollama systemd service...
WARNING: systemd is not running
WARNING: Unable to detect NVIDIA/AMD GPU. Install lspci or lshw to automatically detect and install GPU dependencies.
>>> The Ollama API is now available at 127.0.0.1:11434.
>>> Install complete. Run "ollama" from the command line.
```

## Instructions

>> docker compose build

>> docker-compose up -d

>> docker exec ollama-server ollama pull llama3.2:3b

## Container Architecture

```
┌─────────────────┐    HTTP    ┌─────────────────┐
│   test-app      │ ────────▶ │   ollama        │
│   Flask Web UI  │           │   LLM Server    │
│   Port: 8080    │           │   Port: 11434   │
└─────────────────┘           └─────────────────┘
         │                             │
         ▼                             ▼
   Docker Network              Persistent Volume
   (ollama-docker-test)        (model storage)
```

## Testing Commands

Check status
curl http://localhost:8080/api/status

## Test API directly

curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2:3b","prompt":"Hello!","stream":false}'

# Interactive chat
docker exec -it ollama-server ollama run llama3.2:3b
