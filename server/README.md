# API Server

## Development

### Prerequisites

- [Python](https://www.python.org/downloads/)

### Setup

1. Navigate to this directory:
   ```sh
   cd server
   ```
1. Create a virtual environment:
   ```sh
   python -m venv .venv
   ```
1. Activate the virtual environment:

   Linux/macOS:

   ```sh
   source .venv/bin/activate
   ```

   Windows PowerShell:

   ```cmd
   .venv\Scripts\activate.ps1
   ```

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Run

1. Activate the virtual environment (if not already activated), see above.

1. Run the server:

   Development, server reloads on code changes:

   ```sh
   fastapi dev
   ```

   Production, server does not reload on code changes:

   ```sh
   fastapi start
   ```

1. The server will be running at http://127.0.0.1:8000.

Optionally the host and port can be changed with the `--host` and `--port` options respectively.

## Live Documentation

The API documentation is available at http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc when the server is running. This includes an interactive API explorer. OpenAPI JSON is available at http://127.0.0.1:8000/openapi.json.

## Deployment

To be determined.
