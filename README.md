# ai-trading-agent

ai trading agent using interactive brokers api via browser-use

Uses my Interactive Brokers API Web Application in this repository:

https://github.com/hackingthemarkets/interactive-brokers-web-api

## Bring up the Interactive Brokers Web API Container

```
cd ~/Projects
git clone https://github.com/hackingthemarkets/interactive-brokers-web-api.git
set environment variable for IBKR_ACCOUNT_ID
docker-compose up
authenticate with paper trading or live trading
```

## Set up the Agent dependencies

```
cd ~/Projects
git clone https://github.com/hackingthemarkets/ai-trading-agents
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Carefully study and craft prompts before running the agent. Do this with paper trading to study how it works.

```
python3 agent.py
```

