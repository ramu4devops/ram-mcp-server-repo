# Insecure Model Context Protocol (Insecure-MCP)

```
git clone https://gitlab.practical-devsecops.training/marudhamaran/cmcp-insecure-mcp-server.git
cd cmcp-insecure-mcp-server
docker build -t insecure-mcp .
docker run -p 9001-9010:9001-9010 -p 8001-8010:8001-8010 insecure-mcp
```

Forked from https://github.com/harishsg993010/damn-vulnerable-MCP-server