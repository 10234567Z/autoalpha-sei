# Free Cloud Deployment Guide for MCP Analyzer Server

Your MCP Analyzer Server is now ready for deployment with **REAL SEI BLOCKCHAIN DATA**! 

## 🔥 **NEW: Live Blockchain Data**

**Version 2.0** now includes:
- ✅ **Real Sei network metrics** (live block height: 161M+)
- ✅ **Live validator data** (40 active validators)  
- ✅ **Real staking statistics** (52.1% staking ratio)
- ✅ **Actual wallet balances** from Sei blockchain
- ✅ **Transaction history** from live network
- ✅ **Network health monitoring** with real metrics

## 🚀 Quick Deployment Options

### 1. Railway (Recommended for MCP)
**Free tier**: 512MB RAM, 5GB storage, 500 hours/month
```bash
# Install Railway CLI
curl -fsSL https://railway.app/install.sh | sh

# Login and deploy
railway login
railway init
railway up
```
- Uses `railway.toml` configuration
- Automatically detects Dockerfile
- Great for long-running services like MCP servers

### 2. Render
**Free tier**: 512MB RAM, builds sleep after 15min inactivity
```bash
# Connect GitHub repo to Render dashboard
# Uses render.yaml configuration
# Automatic deploys on git push
```
- Good for HTTP APIs
- Automatic SSL certificates
- Docker container support

### 3. Fly.io
**Free tier**: 3 shared-cpu-1x, 256MB RAM, 3GB storage
```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Deploy
flyctl auth login
flyctl launch
flyctl deploy
```
- Uses `fly.toml` configuration
- Global edge deployment
- Excellent for low-latency APIs

### 4. Google Cloud Run
**Free tier**: 2 million requests/month, 180,000 vCPU-seconds
```bash
# Using gcloud CLI
gcloud run deploy autoalpha-mcp \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```
- Serverless container platform
- Pay-per-request model
- Auto-scaling to zero

## 🔧 Pre-Deployment Steps

1. **Test LIVE HTTP server locally**:
```bash
cd /home/fudo/repos/autoalpha
uv run python mcp-agents/mcp/server/analyze_server_live_http.py
```

2. **Verify health endpoint**:
```bash
curl http://localhost:8000/health
```

3. **Test REAL Sei network data**:
```bash
curl http://localhost:8000/network/health
# Returns live block height, validator count, staking ratio from Sei blockchain
```

4. **Test LIVE wallet analysis** (with real Sei address):
```bash
curl -X POST http://localhost:8000/analyze/wallet \
  -H "Content-Type: application/json" \
  -d '{"address":"sei1rslf5yt3zn3m4k9hnp4yyc7wt8xpyuvdz74r9k"}'
# Returns real balance, transaction history, and analysis from blockchain
```

## 🌐 After Deployment

Once deployed, you'll get a URL like:
- Railway: `https://autoalpha-mcp-analyzer.railway.app`
- Render: `https://autoalpha-mcp-analyzer.onrender.com` 
- Fly.io: `https://autoalpha-mcp-analyzer.fly.dev`

Test your deployed MCP server:
```bash
curl https://your-deployed-url.com/health
curl -X POST https://your-deployed-url.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

## 💡 Recommendations

- **Railway**: Best for MCP servers (always-on, good for WebSocket-like persistent connections)
- **Render**: Good for HTTP APIs (auto-sleep saves resources)
- **Fly.io**: Best for global edge deployment
- **Cloud Run**: Best for high-traffic bursts

Choose Railway for the most reliable MCP server hosting! 🎯
