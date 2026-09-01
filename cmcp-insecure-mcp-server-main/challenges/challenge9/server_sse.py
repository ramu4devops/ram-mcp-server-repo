from mcp.server.fastmcp import FastMCP, Context
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
import subprocess

# Create a vulnerable MCP server for Challenge 9: Remote Access Control with SSE support
class Challenge9Server:
    def __init__(self):
        self.name = "Challenge 9 - Remote Access Control"
        self.port = 9009  # Changed from 8009 to avoid conflicts
        self.mcp = FastMCP(self.name)
        self.app = FastAPI()
        self.app.add_middleware(CORSMiddleware, allow_origins=["*"])

        # Create a directory for network diagnostics logs
        os.makedirs("/tmp/dvmcp_challenge9/logs", exist_ok=True)

        # Add a resource with information about the network
        @self.mcp.resource("network://info")
        def get_network_info() -> str:
            """Information about the network configuration"""
            return """
        NETWORK CONFIGURATION
        --------------------
        Server IP: 192.168.1.100
        Subnet Mask: 255.255.255.0
        Gateway: 192.168.1.1
        DNS Servers: 8.8.8.8, 8.8.4.4
        Firewall: Enabled (Allowing ports 22, 80, 443, 8000-8010)

        Available Tools:
        - ping_host: Check connectivity to a host
        - traceroute: Trace the route to a host
        - port_scan: Check if a port is open on a host
        - network_diagnostic: Run comprehensive network diagnostics
        """

        # Add a vulnerable tool to ping a host
        @self.mcp.tool()
        def ping_host(host: str, count: int = 4) -> str:
            """Ping a host to check connectivity.
            
            Args:
                host: The hostname or IP address to ping
                count: Number of ping packets to send (default: 4)
           
            Returns:
                The result of the ping command
            """
            # VULNERABILITY: This tool passes user input directly to a shell command
            # without proper validation, allowing command injection
            
            try:
                # Attempt at input validation (but insufficient)
                if not (0 < count <= 10):
                    return "Error: Count must be between 1 and 10."
                
                # Vulnerable command construction
                command = f"ping -c {count} {host}"
                
                # Execute the command
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                
                # Log the command and result
                with open("/tmp/dvmcp_challenge9/logs/ping.log", "a") as f:
                    f.write(f"Command: {command}\n")
                    f.write(f"Result: {result.decode()}\n")
                    f.write("-" * 50 + "\n")
                
                return f"Ping result:\n\n{result.decode()}"
            except subprocess.CalledProcessError as e:
                return f"Error executing ping: {e.output.decode()}"
            except Exception as e:
                return f"Error: {str(e)}"

        # Add a vulnerable tool to trace the route to a host
        @self.mcp.tool()
        def traceroute(host: str) -> str:
            """Trace the network route to a host.
            
            Args:
                host: The hostname or IP address to trace
            
            Returns:
                The result of the traceroute command
            """
            # VULNERABILITY: This tool passes user input directly to a shell command
            # without proper validation, allowing command injection
            
            try:
                # Vulnerable command construction
                command = f"traceroute {host}"
                
                # Execute the command
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                
                # Log the command and result
                with open("/tmp/dvmcp_challenge9/logs/traceroute.log", "a") as f:
                    f.write(f"Command: {command}\n")
                    f.write(f"Result: {result.decode()}\n")
                    f.write("-" * 50 + "\n")
                
                return f"Traceroute result:\n\n{result.decode()}"
            except subprocess.CalledProcessError as e:
                return f"Error executing traceroute: {e.output.decode()}"
            except Exception as e:
                return f"Error: {str(e)}"

        # Add a vulnerable tool to scan a port
        @self.mcp.tool()
        def port_scan(host: str, port: int) -> str:
            """Check if a specific port is open on a host.
            
            Args:
                host: The hostname or IP address to scan
                port: The port number to check
            
            Returns:
                Whether the port is open or closed
            """
            # VULNERABILITY: This tool passes user input directly to a shell command
            # without proper validation, allowing command injection
            
            try:
                # Attempt at input validation (but insufficient)
                if not (0 <= port <= 65535):
                    return "Error: Port must be between 0 and 65535."
                
                # Vulnerable command construction using nc (netcat)
                command = f"nc -zv -w 2 {host} {port}"
                
                # Execute the command
                try:
                    result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                    status = "open"
                except subprocess.CalledProcessError as e:
                    result = e.output
                    status = "closed"
                
                # Log the command and result
                with open("/tmp/dvmcp_challenge9/logs/portscan.log", "a") as f:
                    f.write(f"Command: {command}\n")
                    f.write(f"Result: {result.decode()}\n")
                    f.write("-" * 50 + "\n")
                
                return f"Port scan result for {host}:{port}:\n\nStatus: {status}\n\n{result.decode()}"
            except Exception as e:
                return f"Error: {str(e)}"
        
        # Add a highly vulnerable tool for comprehensive network diagnostics
        @self.mcp.tool()
        def network_diagnostic(target: str, options: str = "") -> str:
            """Run comprehensive network diagnostics on a target.
            
            This tool runs multiple network diagnostic commands on the specified target.
            
            Args:
                target: The hostname or IP address to diagnose
                options: Additional options for the diagnostic (optional)
            
            Returns:
                The results of the network diagnostic
            """
            # VULNERABILITY: This tool passes user input directly to a shell command
            # and even allows specifying additional options, making command injection trivial
            
            try:
                # Construct the diagnostic command
                # This is EXTREMELY vulnerable as it directly passes user input to the shell
                # including arbitrary options
                command = f"./network_diagnostic.sh {target} {options}"
                
                # Create the diagnostic script if it doesn't exist
                script_path = "./network_diagnostic.sh"
                if not os.path.exists(script_path):
                    with open(script_path, "w") as f:
                        f.write("""#!/bin/bash
        # Network diagnostic script
        echo "Running network diagnostics on $1"
        echo "Options: $2"
        echo ""
        echo "PING TEST:"
        ping -c 2 $1
        echo ""
        echo "TRACEROUTE:"
        traceroute $1
        echo ""
        echo "DNS LOOKUP:"
        nslookup $1
        echo ""
        echo "Diagnostics completed."
        """)
                    os.chmod(script_path, 0o755)
                
                # Execute the command
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                
                # Log the command and result
                with open("/tmp/dvmcp_challenge9/logs/diagnostic.log", "a") as f:
                    f.write(f"Command: {command}\n")
                    f.write(f"Result: {result.decode()}\n")
                    f.write("-" * 50 + "\n")
                
                return f"Network diagnostic results:\n\n{result.decode()}"
            except subprocess.CalledProcessError as e:
                return f"Error executing network diagnostic: {e.output.decode()}"
            except Exception as e:
                return f"Error: {str(e)}"

        # Add a tool to view network logs
        @self.mcp.tool()
        def view_network_logs(log_type: str = "ping") -> str:
            """View network diagnostic logs.
            
            Args:
                log_type: Type of log to view (ping, traceroute, portscan, diagnostic)
            
            Returns:
                The contents of the specified log file
            """
            try:
                log_files = {
                    "ping": "/tmp/dvmcp_challenge9/logs/ping.log",
                    "traceroute": "/tmp/dvmcp_challenge9/logs/traceroute.log",
                    "portscan": "/tmp/dvmcp_challenge9/logs/portscan.log",
                    "diagnostic": "/tmp/dvmcp_challenge9/logs/diagnostic.log"
                }
                
                if log_type not in log_files:
                    return f"Error: Log type '{log_type}' not recognized. Available types: ping, traceroute, portscan, diagnostic"
                
                log_path = log_files[log_type]
                
                if not os.path.exists(log_path):
                    return f"No {log_type} logs found."
                
                with open(log_path, "r") as f:
                    content = f.read()
                
                return f"{log_type.upper()} LOGS:\n\n{content}"
            except Exception as e:
                return f"Error reading logs: {str(e)}"
        
        # Mount the SSE server
        self.mount_sse_server()
    
    def mount_sse_server(self):
        """Mount the SSE server to the FastAPI app"""
        self.app.mount("/", self.create_sse_server())
        
    def create_sse_server(self):
        """Create a Starlette app that handles SSE connections and message handling"""
        transport = SseServerTransport("/messages/")
        
        # Define handler functions
        async def handle_sse(request):
            async with transport.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await self.mcp._mcp_server.run(
                    streams[0], streams[1], self.mcp._mcp_server.create_initialization_options()
                )
            return Response(status_code=204)
        
        # Create Starlette routes for SSE and message handling
        routes = [
            Route("/sse", endpoint=handle_sse),
            Mount("/messages", app=transport.handle_post_message),
        ]
        
        # Create a Starlette app
        return Starlette(routes=routes)
    
    def run(self):
        """Run the server with uvicorn"""
        import uvicorn
        print(f"Starting {self.name} MCP Server")
        print("Connect to this server using an MCP client (e.g., Claude Desktop or Cursor)")
        print(f"Server running at http://localhost:{self.port}")
        print(f"SSE endpoint available at http://localhost:{self.port}/sse")
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)

# Run the server
if __name__ == "__main__":
    server = Challenge9Server()
    server.run()