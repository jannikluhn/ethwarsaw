### Made during ETHWarsaw 2023 hackathon

# Team

Dina, Markus, Gabriel, Jan, Jannik

# Components

## Telegram Bot

To run the Telegram Bot, perform the following steps is `/packages/telegram/`:

- create and activate a virtual environment
- run `pip install -r requirements.txt`
- create a `.env` file according to `.env.example`, in particular setting `TELEGRAM_BOT_TOKEN` to the token of the Telegram bot
- run `python main.py`

## Chain Monitoring

To run the chain monitor(s), perform the following steps is `/packages/monitoring/`, once per chain that is supported (e.g., Celo and Mantle):

- create and activate a virtual environment
- run `pip install -r requirements.txt`
- create a `.env` file according to `.env.example`, in particular setting `CHAIN_ID` and `JSON_RPC_URL` according to the connected chain
- define which on-chain actions to reward with creatures in the `rules.json` file, by specifying a contract event as well as:
- run `python main.py`

##
