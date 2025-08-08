#!/usr/bin/env python3
"""
HTTP wrapper for the Live Sei Network Analyzer
Uses real Sei blockchain data via HTTP API
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

# Add the MCP server directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our live MCP server components
from analyze_server_live import SeiLiveAnalyzer

# Create FastAPI app
app = FastAPI(
    title="Sei Network Live Analyzer API",
    description="HTTP API for real-time Sei blockchain analysis",
    version="2.0.0"
)

# Initialize live analyzer
analyzer = SeiLiveAnalyzer()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sei Network Live Analyzer API", 
        "status": "running",
        "version": "2.0.0",
        "data_source": "live_sei_blockchain"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "sei-network-live-analyzer"}

@app.post("/analyze/wallet")
async def analyze_wallet_endpoint(request: Request):
    """Analyze a single wallet address using live blockchain data"""
    try:
        body = await request.json()
        address = body.get("address")
        
        if not address:
            raise HTTPException(status_code=400, detail="Address is required")
        
        # Get real account data directly
        account_info = await analyzer.get_account_info(address)
        
        if "error" in account_info:
            raise HTTPException(status_code=500, detail=account_info["error"])
        
        # Get transaction history
        transactions = await analyzer.get_transactions(address, limit=100)
        
        balance = account_info["balance_sei"]
        
        # Calculate metrics using real data
        whale_score = balance / 10000000  # Score based on 10M SEI threshold
        whale_score = min(whale_score, 1.0)
        
        # Risk analysis based on transaction patterns
        risk_factor = 0.3  # Default low risk
        if len(transactions) > 1000:
            risk_factor += 0.3  # High activity
        
        failed_txs = len([tx for tx in transactions if tx.get("status") == "failed"])
        if failed_txs > len(transactions) * 0.1:
            risk_factor += 0.2  # High failure rate
        
        risk_factor = min(risk_factor, 1.0)
        
        # Calculate influence based on transaction volume
        total_volume = sum(tx.get("amount", 0) for tx in transactions)
        influence_score = min(total_volume / balance if balance > 0 else 0, 1.0) * 0.5
        
        # Analyze transaction patterns
        staking_txs = [tx for tx in transactions if tx.get("tx_type") == "staking"]
        reward_txs = [tx for tx in transactions if tx.get("tx_type") == "rewards"]
        
        # Classification
        if whale_score > 0.8:
            classification = "Whale"
        elif whale_score > 0.5:
            classification = "Large Holder"
        elif len(staking_txs) > 10:
            classification = "Active Staker"
        elif len(transactions) > 100:
            classification = "Active Trader"
        else:
            classification = "Regular User"
        
        result = {
            "address": address,
            "analysis_timestamp": datetime.now().isoformat(),
            "classification": classification,
            "real_data": True,
            "scores": {
                "whale_score": round(whale_score, 3),
                "risk_factor": round(risk_factor, 3),
                "influence_score": round(influence_score, 3),
                "overall_score": round((whale_score * 0.4 + (1-risk_factor) * 0.3 + influence_score * 0.3), 3)
            },
            "wallet_metrics": {
                "balance_sei": balance,
                "balance_usei": account_info["balance_usei"],
                "transaction_count": len(transactions),
                "account_number": account_info.get("account_number"),
                "sequence": account_info.get("sequence"),
                "staking_transactions": len(staking_txs),
                "reward_transactions": len(reward_txs)
            },
            "transaction_analysis": {
                "total_transactions": len(transactions),
                "successful_transactions": len([tx for tx in transactions if tx.get("status") == "success"]),
                "failed_transactions": failed_txs,
                "total_volume_sei": round(total_volume, 6),
                "average_transaction_amount": round(total_volume / len(transactions), 6) if transactions else 0,
                "latest_transaction": transactions[0].get("timestamp") if transactions else None
            },
            "recent_transactions": transactions[:5],  # Last 5 transactions
            "recommendations": [r for r in [
                "High-value wallet - monitor for large movements" if whale_score > 0.7 else None,
                "Active staker - earning rewards" if len(staking_txs) > 5 else None,
                "Consider staking for rewards" if len(staking_txs) == 0 and balance > 1000 else None,
                "High transaction failure rate" if failed_txs > len(transactions) * 0.1 else None
            ] if r is not None]
        }
            
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/compare")
async def compare_wallets_endpoint(request: Request):
    """Compare multiple wallet addresses using live blockchain data"""
    try:
        body = await request.json()
        addresses = body.get("addresses", [])
        
        if not addresses or len(addresses) < 2:
            raise HTTPException(status_code=400, detail="At least 2 addresses required")
        
        # Import and use the live comparison function
        from analyze_server_live import compare_sei_addresses
        result = await compare_sei_addresses(addresses)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/network/health")
async def network_health_endpoint():
    """Get live Sei network health status"""
    try:
        # Get network stats directly from analyzer
        network_stats = await analyzer.get_network_stats()
        
        # Calculate health score
        staking_ratio = network_stats.get("staking_ratio", 0.65)
        active_validators = network_stats.get("active_validators", 100)
        
        health_score = (
            min(staking_ratio / 0.6, 1.0) * 0.4 +  # Target 60%+ staking
            min(active_validators / 80, 1.0) * 0.4 +  # Target 80+ validators
            0.2  # Base score
        )
        
        health_status = "Excellent" if health_score > 0.9 else "Good" if health_score > 0.7 else "Fair"
        
        result = {
            "network_health": {
                "overall_score": round(health_score, 3),
                "status": health_status,
                "chain_id": network_stats.get("chain_id", "pacific-1"),
                "last_updated": datetime.now().isoformat()
            },
            "live_metrics": network_stats,
            "analysis": {
                "staking_participation": f"{staking_ratio:.1%}",
                "validator_count": active_validators,
                "network_security": "High" if staking_ratio > 0.6 else "Medium",
                "latest_block": network_stats.get("block_height", 0)
            },
            "real_data": True,
            "data_source": "sei-blockchain-apis"
        }
            
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/network/stats")
async def network_stats_endpoint():
    """Get detailed Sei network statistics"""
    try:
        stats = await analyzer.get_network_stats()
        return JSONResponse(content={
            "network_stats": stats,
            "real_data": True,
            "timestamp": analyzer._network_cache.get("network_stats", {}).get("timestamp")
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/account/{address}")
async def get_account_endpoint(address: str):
    """Get basic account information"""
    try:
        account_info = await analyzer.get_account_info(address)
        
        if "error" in account_info:
            raise HTTPException(status_code=404, detail=account_info["error"])
            
        return JSONResponse(content=account_info)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/transactions/{address}")
async def get_transactions_endpoint(address: str, limit: int = 50):
    """Get transaction history for an address"""
    try:
        if limit > 200:
            limit = 200  # Maximum limit
            
        transactions = await analyzer.get_transactions(address, limit)
        
        return JSONResponse(content={
            "address": address,
            "transactions": transactions,
            "count": len(transactions),
            "limit": limit,
            "real_data": True
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """MCP JSON-RPC endpoint for compatibility with live data"""
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id", 1)
        
        if method == "tools/list":
            result = {
                "tools": [
                    {
                        "name": "analyze_wallet_live",
                        "description": "Comprehensive analysis of a Sei wallet using real blockchain data"
                    },
                    {
                        "name": "compare_sei_addresses", 
                        "description": "Compare multiple Sei addresses using live blockchain data"
                    },
                    {
                        "name": "get_sei_network_health",
                        "description": "Get real-time Sei network health and statistics"
                    }
                ]
            }
            
        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name == "analyze_wallet_live":
                from analyze_server_live import analyze_wallet_live
                address = tool_args.get("address")
                if not address:
                    raise HTTPException(status_code=400, detail="Address is required")
                result = await analyze_wallet_live(address)
                
            elif tool_name == "compare_sei_addresses":
                from analyze_server_live import compare_sei_addresses
                addresses = tool_args.get("addresses", [])
                if len(addresses) < 2:
                    raise HTTPException(status_code=400, detail="At least 2 addresses required")
                result = await compare_sei_addresses(addresses)
                
            elif tool_name == "get_sei_network_health":
                from analyze_server_live import get_sei_network_health
                result = await get_sei_network_health()
                
            else:
                raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown method: {method}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    except HTTPException as e:
        return {
            "jsonrpc": "2.0",
            "id": body.get("id", 1) if 'body' in locals() else 1,
            "error": {
                "code": e.status_code,
                "message": str(e.detail)
            }
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
