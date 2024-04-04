import json
import random
from typing import Any
from pybit.unified_trading import HTTP


def load_config(filename: str) -> Any:
    """ loads file with data about accounts """
    with open(filename, 'r') as file:
        return json.load(file)


def generate_order_value(balance: float) -> float:
    """ generates randon order value between user balance and balance - 10 """
    return round(random.uniform(balance * 0.9, balance), 2)


def get_wallet_balance(session: HTTP, coin: str) -> float:
    """ returns wallet balance of coin from SPOT account"""
    wallet_balance_response = session.get_wallet_balance(accountType="SPOT", coin=coin)
    wallet_balance = wallet_balance_response.get('result', {}).get('list', [{}])[0].get('coin', [{}])[0].get('walletBalance')
    return float(wallet_balance)


def main():
    config = load_config("config.json")
    number_of_transactions = 20     # number of transacitons to make trade volume
    transaction_volume = 0

    for account_name, account_config in config.items():
        api_key = account_config["api_key"]
        api_secret = account_config["api_secret"]
        # proxy = account_config.get("proxy")
        # proxy_login = account_config.get("proxy_login")
        # proxy_pass = account_config.get("proxy_pass")
        # user_agent = account_config.get("user_agent")

        session = HTTP(
            testnet=False,  # Set to True if using testnet
            api_key=api_key,
            api_secret=api_secret
            # proxy=proxy,
            # proxy_login=proxy_login,
            # proxy_pass=proxy_pass,
            # user_agent=user_agent
        )

        is_buy = True   # Toggle variable to switch between "Buy" and "Sell"

        for _ in range(number_of_transactions):
            side, coin = ("Buy", "USDT") if is_buy else ("Sell", "USDC")    # select side and coin to trade 
            
            wallet_balance = get_wallet_balance(session, coin)

            transaction_size = generate_order_value(wallet_balance)

            # Place an order at market price for USDT/USDC pair
            order_response = session.place_order(
                category="spot",
                symbol="USDCUSDT",
                side=side,
                orderType="Market",
                qty=str(transaction_size)
            )
            print(f"Order response for account '{account_name}':")
            print(order_response)

            print(f"Transaction size: {transaction_size}")

            transaction_volume += transaction_size
            
            is_buy = not is_buy     # Toggle the side for the next transaction

    print(f"Transaction Volume for {account_name}:{transaction_volume}")   # the +- transaction volume for account 

if __name__ == "__main__":
    main()
