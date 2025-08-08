#!/usr/bin/env python3
"""
Comprehensive Sei Network Analyzer MCP Server
Provides detailed wallet analysis, network health monitoring, and address comparison tools.
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import statistics

from mcp.server.fastmcp import FastMCP

# Create server instance
mcp = FastMCP("sei-network-analyzer")


class SeiAnalyzer:
    """
    Comprehensive Sei Network Analyzer for wallet and transaction analysis
    """
    
    def __init__(self):
        self.sei_metrics = {
            "average_block_time": 0.5,  # ~500ms
            "network_tps": 20000,       # 20k TPS capability
            "validator_count": 100,      # Approximate validator count
            "staking_ratio": 0.65,      # 65% of tokens staked
            "inflation_rate": 0.08      # 8% annual inflation
        }
    
    def calculate_whale_score(self, balance: float, total_supply: float = 10_000_000_000) -> float:
        """Calculate whale score based on token holdings"""
        if balance <= 0:
            return 0.0
        
        percentage_of_supply = (balance / total_supply) * 100
        
        if percentage_of_supply >= 1.0:
            return 1.0  # Mega whale
        elif percentage_of_supply >= 0.1:
            return 0.9  # Large whale
        elif percentage_of_supply >= 0.01:
            return 0.7  # Medium whale
        elif percentage_of_supply >= 0.001:
            return 0.5  # Small whale
        elif percentage_of_supply >= 0.0001:
            return 0.3  # Dolphin
        else:
            return 0.1  # Fish
    
    def calculate_risk_factor(self, transactions: List[Dict], balance: float) -> float:
        """Calculate risk factor based on transaction patterns"""
        if not transactions:
            return 0.5  # Neutral risk for no transactions
        
        risk_factors = []
        
        # Transaction frequency analysis
        tx_count = len(transactions)
        if tx_count > 1000:
            risk_factors.append(0.8)  # High frequency could be bot
        elif tx_count > 100:
            risk_factors.append(0.6)  # Medium frequency
        else:
            risk_factors.append(0.3)  # Low frequency
        
        # Transaction amount analysis
        amounts = [float(tx.get('amount', 0)) for tx in transactions]
        if amounts:
            avg_amount = statistics.mean(amounts)
            max_amount = max(amounts)
            
            # High value transactions increase risk
            if max_amount > balance * 0.5:
                risk_factors.append(0.7)
            elif avg_amount > balance * 0.1:
                risk_factors.append(0.6)
            else:
                risk_factors.append(0.3)
        
        # Pattern analysis
        unique_counterparties = set()
        for tx in transactions:
            if 'from' in tx:
                unique_counterparties.add(tx['from'])
            if 'to' in tx:
                unique_counterparties.add(tx['to'])
        
        counterparty_ratio = len(unique_counterparties) / max(tx_count, 1)
        if counterparty_ratio < 0.1:
            risk_factors.append(0.8)  # Very few counterparties - suspicious
        elif counterparty_ratio < 0.3:
            risk_factors.append(0.6)  # Limited counterparties
        else:
            risk_factors.append(0.3)  # Good distribution
        
        return min(statistics.mean(risk_factors), 1.0)
    
    def calculate_influence_score(self, transactions: List[Dict], balance: float) -> float:
        """Calculate on-chain influence based on transaction volume and network participation"""
        if not transactions:
            return 0.1
        
        # Volume-based influence
        total_volume = sum(float(tx.get('amount', 0)) for tx in transactions)
        volume_score = min(total_volume / (balance * 10), 1.0) * 0.4
        
        # Activity-based influence
        tx_count = len(transactions)
        activity_score = min(tx_count / 1000, 1.0) * 0.3
        
        # Network participation (based on unique interactions)
        unique_addresses = set()
        for tx in transactions:
            if 'from' in tx:
                unique_addresses.add(tx['from'])
            if 'to' in tx:
                unique_addresses.add(tx['to'])
        
        network_score = min(len(unique_addresses) / 100, 1.0) * 0.3
        
        return min(volume_score + activity_score + network_score, 1.0)
    
    def analyze_transaction_patterns(self, transactions: List[Dict]) -> Dict:
        """Analyze transaction patterns for insights"""
        if not transactions:
            return {"pattern": "no_activity", "description": "No transactions found"}
        
        # Time-based analysis
        tx_count = len(transactions)
        
        # Amount analysis
        amounts = [float(tx.get('amount', 0)) for tx in transactions]
        if amounts:
            avg_amount = statistics.mean(amounts)
            median_amount = statistics.median(amounts)
            max_amount = max(amounts)
            min_amount = min(amounts)
        else:
            avg_amount = median_amount = max_amount = min_amount = 0
        
        # Direction analysis
        incoming = sum(1 for tx in transactions if tx.get('type') == 'incoming')
        outgoing = sum(1 for tx in transactions if tx.get('type') == 'outgoing')
        
        patterns = []
        
        if tx_count > 1000:
            patterns.append("high_frequency_trader")
        elif incoming > outgoing * 2:
            patterns.append("accumulator")
        elif outgoing > incoming * 2:
            patterns.append("distributor")
        elif avg_amount > median_amount * 3:
            patterns.append("irregular_amounts")
        else:
            patterns.append("regular_user")
        
        return {
            "primary_pattern": patterns[0] if patterns else "unknown",
            "transaction_count": tx_count,
            "average_amount": avg_amount,
            "median_amount": median_amount,
            "max_amount": max_amount,
            "incoming_ratio": incoming / max(tx_count, 1),
            "outgoing_ratio": outgoing / max(tx_count, 1),
            "patterns": patterns
        }
    
    def get_sei_specific_metrics(self, address: str, transactions: List[Dict]) -> Dict:
        """Calculate Sei-specific metrics"""
        
        # Simulate staking analysis
        staking_txs = [tx for tx in transactions if 'staking' in tx.get('type', '').lower()]
        delegation_amount = sum(float(tx.get('amount', 0)) for tx in staking_txs)
        
        # DeFi participation (simulate based on contract interactions)
        defi_txs = [tx for tx in transactions if tx.get('to', '').startswith('sei1')]
        defi_participation = len(defi_txs) > 0
        
        # Calculate SEI-specific scores
        sei_network_score = 0.5  # Base score
        
        if delegation_amount > 0:
            sei_network_score += 0.2  # Bonus for staking
        
        if defi_participation:
            sei_network_score += 0.2  # Bonus for DeFi usage
        
        if len(transactions) > 50:
            sei_network_score += 0.1  # Bonus for active usage
        
        return {
            "staking_amount": delegation_amount,
            "defi_participation": defi_participation,
            "sei_network_score": min(sei_network_score, 1.0),
            "estimated_rewards": delegation_amount * self.sei_metrics["inflation_rate"] * 0.85,  # 85% of inflation rate
            "validator_interactions": len(staking_txs)
        }


# Initialize analyzer
analyzer = SeiAnalyzer()


@mcp.tool()
async def analyze_wallet(walletData: dict) -> dict:
    """
    Comprehensive Sei wallet analysis including risk assessment, whale scoring, and network influence.
    
    Args:
        walletData (dict): Wallet data containing address, balance, and transactions
            - address (str): The wallet address
            - balance (str/float): Current balance in SEI
            - transactions (list): List of transactions with details
    
    Returns:
        dict: Comprehensive analysis including risk factors, whale score, influence metrics, and Sei-specific data
    """
    
    # Extract data
    address = walletData.get('address', 'unknown')
    balance = float(walletData.get('balance', 0))
    transactions = walletData.get('transactions', [])
    
    # Core analysis
    whale_score = analyzer.calculate_whale_score(balance)
    risk_factor = analyzer.calculate_risk_factor(transactions, balance)
    influence_score = analyzer.calculate_influence_score(transactions, balance)
    
    # Pattern analysis
    patterns = analyzer.analyze_transaction_patterns(transactions)
    
    # Sei-specific metrics
    sei_metrics = analyzer.get_sei_specific_metrics(address, transactions)
    
    # Overall scoring
    overall_score = (whale_score * 0.3 + (1 - risk_factor) * 0.3 + influence_score * 0.4)
    
    # Classification
    if whale_score >= 0.8:
        classification = "Whale"
    elif whale_score >= 0.5:
        classification = "Large Holder"
    elif influence_score >= 0.7:
        classification = "Active Trader"
    elif sei_metrics["defi_participation"]:
        classification = "DeFi User"
    elif sei_metrics["staking_amount"] > 0:
        classification = "Staker"
    else:
        classification = "Regular User"
    
    result = {
        "address": address,
        "analysis_timestamp": datetime.now().isoformat(),
        "classification": classification,
        "scores": {
            "whale_score": round(whale_score, 3),
            "risk_factor": round(risk_factor, 3),
            "influence_score": round(influence_score, 3),
            "overall_score": round(overall_score, 3),
            "sei_network_score": round(sei_metrics["sei_network_score"], 3)
        },
        "wallet_metrics": {
            "balance_sei": balance,
            "transaction_count": len(transactions),
            "estimated_usd_value": balance * 0.45,  # Approximate SEI price
            "balance_percentage_of_supply": (balance / 10_000_000_000) * 100
        },
        "transaction_patterns": patterns,
        "sei_specific": sei_metrics,
        "risk_assessment": {
            "level": "High" if risk_factor > 0.7 else "Medium" if risk_factor > 0.4 else "Low",
            "factors": [f for f in [
                "High transaction frequency" if len(transactions) > 1000 else None,
                "Limited counterparties" if len(set(tx.get('from', '') for tx in transactions)) < len(transactions) * 0.1 else None,
                "Large transaction amounts" if any(float(tx.get('amount', 0)) > balance * 0.5 for tx in transactions) else None
            ] if f is not None]
        },
        "recommendations": [r for r in [
            "Monitor for wash trading" if risk_factor > 0.8 else None,
            "Potential market maker" if influence_score > 0.8 and len(transactions) > 500 else None,
            "Strong network participant" if sei_metrics["sei_network_score"] > 0.8 else None,
            "Consider for validator program" if sei_metrics["staking_amount"] > 1000000 else None
        ] if r is not None]
    }
    
    return result


@mcp.tool()
async def analyze_network_health(networkData: dict = None) -> dict:
    """
    Analyze Sei network health metrics and provide insights.
    
    Args:
        networkData (dict, optional): Network metrics data
    
    Returns:
        dict: Network health analysis
    """
    
    # Simulate real-time network metrics
    current_metrics = {
        "block_height": 12500000,
        "block_time": 0.48,
        "active_validators": 95,
        "total_validators": 100,
        "bonded_tokens": 6500000000,
        "total_supply": 10000000000,
        "current_inflation": 0.078,
        "community_pool": 50000000
    }
    
    # Health scoring
    validator_ratio = current_metrics["active_validators"] / current_metrics["total_validators"]
    staking_ratio = current_metrics["bonded_tokens"] / current_metrics["total_supply"]
    
    network_health_score = (
        (validator_ratio * 0.3) +
        (staking_ratio * 0.4) +
        (1.0 if current_metrics["block_time"] < 1.0 else 0.8) * 0.3
    )
    
    health_status = "Excellent" if network_health_score > 0.9 else "Good" if network_health_score > 0.7 else "Fair"
    
    result = {
        "network_health": {
            "overall_score": round(network_health_score, 3),
            "status": health_status,
            "last_updated": datetime.now().isoformat()
        },
        "metrics": current_metrics,
        "analysis": {
            "validator_participation": f"{validator_ratio:.1%}",
            "network_security": "High" if staking_ratio > 0.6 else "Medium",
            "block_performance": "Optimal" if current_metrics["block_time"] < 0.6 else "Good",
            "decentralization_score": round(validator_ratio * staking_ratio, 3)
        },
        "recommendations": [r for r in [
            "Network is performing optimally" if network_health_score > 0.9 else None,
            "Monitor validator participation" if validator_ratio < 0.9 else None,
            "Encourage more staking" if staking_ratio < 0.6 else None
        ] if r is not None]
    }
    
    return result


@mcp.tool()
async def compare_addresses(addressData: dict) -> dict:
    """
    Compare multiple Sei addresses for similarities and differences.
    
    Args:
        addressData (dict): Dictionary containing multiple addresses and their data
            - addresses (list): List of address data objects to compare
    
    Returns:
        dict: Comparison analysis between addresses
    """
    
    addresses = addressData.get('addresses', [])
    if len(addresses) < 2:
        return {"error": "At least 2 addresses required for comparison"}
    
    comparisons = []
    
    for addr_data in addresses:
        # Reuse the analyze_wallet logic
        analysis = await analyze_wallet(addr_data)
        
        comparisons.append({
            "address": addr_data.get('address', 'unknown'),
            "whale_score": analysis["scores"]["whale_score"],
            "risk_factor": analysis["scores"]["risk_factor"],
            "influence_score": analysis["scores"]["influence_score"],
            "classification": analysis["classification"],
            "balance": float(addr_data.get('balance', 0)),
            "tx_count": len(addr_data.get('transactions', []))
        })
    
    # Find similarities and differences
    whale_scores = [c["whale_score"] for c in comparisons]
    risk_factors = [c["risk_factor"] for c in comparisons]
    
    result = {
        "comparison_summary": {
            "total_addresses": len(addresses),
            "highest_whale_score": max(whale_scores),
            "highest_risk": max(risk_factors),
            "average_whale_score": round(statistics.mean(whale_scores), 3),
            "average_risk": round(statistics.mean(risk_factors), 3)
        },
        "individual_analysis": comparisons,
        "insights": {
            "whale_concentration": len([w for w in whale_scores if w > 0.7]),
            "high_risk_addresses": len([r for r in risk_factors if r > 0.7]),
            "potential_connections": "Manual review recommended" if statistics.stdev(whale_scores) < 0.1 else "No obvious connections"
        }
    }
    
    return result


if __name__ == "__main__":
    mcp.run(transport="stdio")