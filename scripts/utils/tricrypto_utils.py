import os

from etherscan.proxies import Proxies
from etherscan.contracts import Contract
from web3 import Web3

WEB3 = Web3(Web3.HTTPProvider("http://fullnode.dappnode:8545"))
TRICRYPTO_CONTRACT_ADDRESS = "0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785"


def get_erc20_token_into_contract(tx: dict, tx_fetcher: Proxies):

    tricrypto_contract = Contract(
        address=TRICRYPTO_CONTRACT_ADDRESS, api_key=os.environ["ETHERSCAN_API_KEY"]
    )
    tricrypto_contract_abi = tricrypto_contract.get_abi()
    tricrypto_contract_web3 = WEB3.eth.contract(
        address=TRICRYPTO_CONTRACT_ADDRESS, abi=tricrypto_contract_abi
    )
    tx_input = tx["input"]
    decoded_input = tricrypto_contract_web3.decode_function_input(tx_input)
    method_name = decoded_input[0].__dict__["abi"]["name"]

    # only continue if method called was add_liquidity in the contract
    if method_name != "add_liquidity":
        return {}
    tx_amounts = decoded_input[1]["_amounts"]
    input_tokens = {
        "liquidity_added": {
            "USDT": tx_amounts[0],
            "WBTC": tx_amounts[1],
            "ETH": tx_amounts[2],
        }
    }
    return input_tokens


def main():
    from etherscan_utils.contract_interactions import Contract
    import os
    import json

    tx_fetcher = Proxies(api_key=os.environ["ETHERSCAN_API_KEY"])

    tricrypto_contract = Contract(
        address="0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785",
        api_key=os.environ["ETHERSCAN_API_KEY"],
    )
    user = "0xcAf2d3f6c4A375ccEC74eB7eD5c03f5B6cd8876E"

    user_txes = tricrypto_contract.get_tx_with(addr=user.lower())
    for tx in user_txes:
        print("Block Number: ", tx["blockNumber"])
        tokens_added = get_erc20_token_into_contract(tx, tx_fetcher=tx_fetcher)
        print(json.dumps(tokens_added, indent=4))


if __name__ == "__main__":
    main()
