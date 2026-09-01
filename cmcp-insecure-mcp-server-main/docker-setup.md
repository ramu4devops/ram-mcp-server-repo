# Docker Setup for Damn Vulnerable MCP

This document provides instructions for building and running the Damn Vulnerable Model Context Protocol (DVMCP) project using Docker.

## Overview

The Docker container includes all 10 MCP challenge servers running simultaneously in a single container, managed by supervisord. Each challenge server listens on its own port (9001-9010).

## Prerequisites

- Docker installed on your system
- Basic knowledge of Docker commands

## Files

The Docker setup consists of three main files:

1. **Dockerfile**: Defines the container image, including the base image, dependencies, and configuration.
2. **supervisord.conf**: Configures supervisord to manage all 20 MCP challenge servers.
3. **startup.sh**: Initializes the environment for all challenges before starting the servers.

## Building the Docker Image

To build the Docker image:

```bash
docker build -t insecure-mcp .
```

This command builds a Docker image named "insecure-mcp" using the Dockerfile in the current directory.

## Running the Container

To run the container:

```bash
docker run -p 8001-8010:8001-8010 -p 9001-9010:9001-9010 insecure-mcp
```

This command:
- Starts a container from the "insecure-mcp" image
- Maps ports 8001-8010 from the container to the same ports on your host machine
- Maps ports 9001-9010 from the container to the same ports on your host machine
- Runs all 10 MCP challenge servers simultaneously on the SSE
- Runs all 10 MCP challenge servers simultaneously on the HTTP

## Accessing the Challenges

Once the container is running, you can access each challenge using an MCP client (e.g., Claude Desktop or MCP Inspector):

- Challenge 1 (Basic Prompt Injection): http://localhost:8001 (SSE) http://localhost:9001 (HTTP)
- Challenge 2 (Tool Poisoning): http://localhost:8002 (SSE) http://localhost:9002 (HTTP)
- Challenge 3 (Excessive Permission Scope): http://localhost:8003 (SSE) http://localhost:9003 (HTTP)
- Challenge 4 (Rug Pull Attack): http://localhost:8004 (SSE) http://localhost:9004 (HTTP)
- Challenge 5 (Tool Shadowing): http://localhost:8005 (SSE) http://localhost:9005 (HTTP)
- Challenge 6 (Indirect Prompt Injection): http://localhost:8006 (SSE) http://localhost:9006 (HTTP)
- Challenge 7 (Token Theft): http://localhost:8007 (SSE) http://localhost:9007 (HTTP)
- Challenge 8 (Malicious Code Execution): http://localhost:8008 (SSE) http://localhost:9008 (HTTP)
- Challenge 9 (Remote Access Control): http://localhost:8009 (SSE) http://localhost:9009 (HTTP)
- Challenge 10 (Multi-Vector Attack): http://localhost:8010 (SSE) http://localhost:9010 (HTTP)

## Viewing Logs

To view the logs for a specific challenge:

```bash
docker exec -it <container_id> cat /var/log/supervisor/challenge1_sse.log
```

```bash
docker exec -it <container_id> cat /var/log/supervisor/challenge1_http.log
```

Replace `<container_id>` with the actual container ID and `challenge1_sse.log` with the log file for the challenge you want to view.

## Stopping the Container

To stop the running container:

```bash
docker stop <container_id>
```

Replace `<container_id>` with the actual container ID.


## Advanced Usage

### Running in Detached Mode

To run the container in the background:

```bash
docker run -d -p 8001-8010:8001-8010 -p 9001-9010:9001-9010 insecure-mcp
``
