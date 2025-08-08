#!/usr/bin/env python3
"""
HTTP wrapper for the Sei Network Analyzer MCP Server
Simple FastAPI wrapper for cloud deployment
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

# Add the MCP server directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our MCP server components
from analyze_server import SeiAnalyzer, analyzer

# Create FastAPI app
app = FastAPI(
    title="Sei Network Analyzer API",
    description="HTTP API for Sei blockchain wallet analysis",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Sei Network Analyzer API", "status": "running"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "sei-network-analyzer"}

@app.post("/analyze/wallet")
async def analyze_wallet_endpoint(request: Request):
    """Analyze a single wallet address"""
    try:
        body = await request.json()
        address = body.get("address")
        balance = body.get("balance", 1000000)  # Default balance for demo
        transactions = body.get("transactions", [])
        
        if not address:
            raise HTTPException(status_code=400, detail="Address is required")
        
        # Create wallet data in the format expected by the MCP tool
        wallet_data = {
            "address": address,
            "balance": balance,
            "transactions": transactions
        }
        
        # Import the actual MCP tool function 
        from analyze_server import analyze_wallet
        result = await analyze_wallet(wallet_data)
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/compare")
async def compare_wallets_endpoint(request: Request):
    """Compare multiple wallet addresses"""
    try:
        body = await request.json()
        addresses = body.get("addresses", [])
        
        if not addresses or len(addresses) < 2:
            raise HTTPException(status_code=400, detail="At least 2 addresses required")
        
        # Import the actual MCP tool function
        from analyze_server import compare_addresses
        address_data = {"addresses": addresses}
        result = await compare_addresses(address_data)
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/network/health")
async def network_health_endpoint():
    """Get Sei network health status"""
    try:
        # Import the actual MCP tool function
        from analyze_server import analyze_network_health
        result = await analyze_network_health()
        return JSONResponse(content=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """MCP JSON-RPC endpoint for compatibility"""
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id", 1)
        
        if method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": "analyze_wallet",
                        "description": "Comprehensive analysis of a Sei wallet address including risk assessment, whale scoring, and transaction patterns"
                    },
                    {
                        "name": "compare_addresses", 
                        "description": "Compare multiple wallet addresses to identify patterns, connections, and risk factors"
                    },
                    {
                        "name": "analyze_network_health",
                        "description": "Monitor Sei network health, performance metrics, and validator status"
                    }
                ]
            }
            
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name == "analyze_wallet":
                from analyze_server import analyze_wallet
                wallet_data = tool_args.get("walletData", {})
                result = await analyze_wallet(wallet_data)
                
            elif tool_name == "compare_addresses":
                from analyze_server import compare_addresses
                address_data = tool_args.get("addressData", {})
                result = await compare_addresses(address_data)
                
            elif tool_name == "analyze_network_health":
                from analyze_server import analyze_network_health
                result = await analyze_network_health()
                
            else:
                raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {method}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id", 1) if 'body' in locals() else 1,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
