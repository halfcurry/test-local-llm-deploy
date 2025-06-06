
# Local LLM Environment with Ollama and Open WebUI

This project sets up a local Large Language Model (LLM) environment using Docker Compose, featuring:

* **Ollama:** A powerful tool for running open-source LLMs locally.

* **Open WebUI:** A user-friendly web interface to interact with your Ollama models.

* **Test Application:** A placeholder `test-app` service demonstrating dependency on the Ollama server.

Models `llama3.2:3b` and `phi3:mini` will be automatically pulled into your Ollama instance upon initial startup.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Docker Desktop:** (Includes Docker Engine and Docker Compose)

    * [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Getting Started

Follow these steps to set up and run your local LLM environment:

### 1. Save the Docker Compose File

Save the provided `docker-compose.yml` content (the one you selected) into a file named `docker-compose.yml` in your project directory.

### 2. Create the `test-app` directory (if not already present)

The `test-app` service is configured to build from `./test-app`. Create an empty directory named `test-app` in the same directory as your `docker-compose.yml` file. For a functional test app, you would place your `Dockerfile` and application code within this directory. For this POC, an empty directory is sufficient for `docker compose build` to succeed (though `test-app` itself won't be functional without its contents).

```bash
mkdir test-app
````

### 3\. Start the Services

Navigate to your project directory in the terminal and run the following command. This will build necessary images, pull `ollama/ollama` and `open-webui`, start all services, and initiate the model pulling process within the `ollama-server` container.

```bash
docker compose up --build -d
```

  * `--build`: Ensures that the `ollama` service's image is rebuilt, applying the custom command logic.

  * `-d`: Runs the containers in detached mode (in the background).

**Note:** The initial startup may take some time, especially as Ollama downloads `llama3.2:3b` and `phi3:mini` models. You can monitor the progress by checking the Ollama container logs.

### 4\. Monitor Model Pulling (Optional)

To observe the model downloading process within the `ollama-server` container:

```bash
docker logs -f ollama-server
```

You should see messages indicating the Ollama server starting, waiting for readiness, and then pulling the specified models. Look for "Models pulled successfully\!" at the end.

### 5\. Access the Applications

Once all services are up and healthy:

  * **Open WebUI:**
    Access the web interface in your browser at:
    [http://localhost:3000](https://www.google.com/search?q=http://localhost:3000)

    You should see the Open WebUI dashboard where you can select and interact with your `llama3.2:3b` and `phi3:mini` models.

  * **Ollama API:**
    The Ollama API is exposed on port `11434` on your host. You can test it with `curl` (if installed):

    ```bash
    curl http://localhost:11434/api/tags
    ```

    This should list the models that have been pulled.

  * **Test Application:**
    Your `test-app` would typically be accessible on port `8080`. If you've developed a simple web application in `test-app` that uses the Ollama API, you would access it via:
    [http://localhost:8080](https://www.google.com/search?q=http://localhost:8080)

### 6\. Verify Pulled Models

You can directly check which models are available on your Ollama server:

```bash
docker exec -it ollama-server ollama list
```

This command should list `llama3.2:3b` and `phi3:mini` (and any other models you might pull later).

## Stopping and Cleaning Up

To stop and remove all services, networks, and volumes (including downloaded Ollama models and Open WebUI data):

```bash
docker compose down -v
```

  * `down`: Stops and removes containers and networks.

  * `-v`: Removes named volumes, ensuring a clean slate. Use this option with caution as it deletes all downloaded models and chat history.

If you only want to stop the services without removing volumes:

```bash
docker compose down
```
