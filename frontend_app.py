#!/usr/bin/env python3
"""
Simple MCP Chat Interface
"""

import streamlit as st
import subprocess
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="MCP Chat",
    page_icon="🤖",
    layout="wide"
)

def create_json_rpc_request(query: str, request_id: int = 2) -> str:
    """
    Takes a simple string and wraps it in the required JSON-RPC structure.

    Args:
        query (str): The natural language query (e.g., "nebraska").
        request_id (int): A unique ID for the request.

    Returns:
        A JSON-formatted string ready to be sent to the MCP server.
    """
    request_object = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": "firecrawl_search",
            "arguments": {"query": query}
        }
    }
    # Use json.dumps to serialize the Python dictionary into a JSON string.
    return json.dumps(request_object, indent=2)

def send_to_mcp_server(json_rpc_request: str):
    """
    Sends the JSON-RPC request to the MCP server and returns the response.
    Just replicates what works in terminal.
    """
    try:
        # Prepare both requests
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "frontend_app",
                    "version": "1.0.0"
                }
            }
        }
        
        # Try interactive approach with Popen
        process = subprocess.Popen(
            ["node", "firecrawl-mcp-server/dist/index.js"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Users/solidliquidity/Downloads/projects/ai-lending-agent"
        )
        
        # Step 1: Send init and wait for response
        init_json = json.dumps(init_request) + "\n"
        process.stdin.write(init_json)
        process.stdin.flush()
        
        # Read init response
        init_response = process.stdout.readline()
        print(f"DEBUG: Init response: {init_response.strip()}")
        
        # Step 2: Send tool request
        process.stdin.write(json_rpc_request + "\n")
        process.stdin.flush()
        
        # Read tool response
        tool_response = process.stdout.readline()
        print(f"DEBUG: Tool response: {tool_response.strip()}")
        
        # Close and clean up
        process.stdin.close()
        process.wait()
        
        result = type('obj', (object,), {
            'returncode': process.returncode,
            'stdout': init_response + tool_response,
            'stderr': process.stderr.read() if process.stderr else ""
        })()
        
        if result.returncode != 0:
            return {"error": f"MCP server exited with code {result.returncode}: {result.stderr}"}
        
        if not result.stdout.strip():
            return {"error": "No response from MCP server"}
        
        # Debug: let's see what we got back
        print(f"DEBUG: MCP server response:\n{result.stdout}")
        print(f"DEBUG: MCP server stderr:\n{result.stderr}")
        
        # Parse responses
        lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        
        # Filter out only JSON lines
        json_lines = []
        for line in lines:
            try:
                json.loads(line)
                json_lines.append(line)
            except json.JSONDecodeError:
                continue
        
        if len(json_lines) < 2:
            return {"error": f"Incomplete response. Expected 2 JSON responses, got {len(json_lines)}. Full output: {result.stdout}"}
        
        # Return the tool response (last JSON line)
        tool_response = json.loads(json_lines[-1])
        return tool_response
        
    except subprocess.TimeoutExpired:
        return {"error": "MCP server timeout"}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON response: {e}"}
    except Exception as e:
        return {"error": f"Failed to communicate with MCP server: {str(e)}"}

def main():
    st.title("🤖 MCP Chat")
    
    # Check API key
    if not os.getenv("FIRECRAWL_API_KEY"):
        st.error("❌ FIRECRAWL_API_KEY not found")
        st.stop()
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input
    if prompt := st.chat_input("Type your message..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Process and respond
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                json_rpc_request = create_json_rpc_request(prompt)
                response = send_to_mcp_server(json_rpc_request)
                
                if "error" in response:
                    response_text = f"❌ Error: {response['error']}"
                elif "result" in response and response["result"].get("content"):
                    # Extract the actual content from the MCP response
                    content = response["result"]["content"]
                    if isinstance(content, list) and len(content) > 0:
                        response_text = content[0].get("text", "No content returned")
                    else:
                        response_text = str(content)
                else:
                    response_text = f"Unexpected response format: {response}"
                
                st.write(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

if __name__ == "__main__":
    main()