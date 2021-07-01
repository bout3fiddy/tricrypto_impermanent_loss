import os

from etherscan.contracts import Contract
from web3 import Web3

WEB3 = Web3(Web3.HTTPProvider("http://fullnode.dappnode:8545"))
TRICRYPTO_CONTRACT_ADDRESS = "0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785"


def get_added_liquidity(tx: dict):

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
            "USDT": tx_amounts[0] / 10 ** 7,
            "WBTC": tx_amounts[1] / 10 ** 8,
            "ETH": tx_amounts[2] / 10 ** 18,
        }
    }
    return input_tokens


def main():
    from etherscan_utils.contract_interactions import Contract
    import os
    import json

    tricrypto_contract = Contract(
        address="0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785",
        api_key=os.environ["ETHERSCAN_API_KEY"],
    )
    user = "0x0716266cc5d3c443e30b0c4e9c72afa33778e1de"

    user_txes = tricrypto_contract.get_tx_with(addr=user.lower())
    for tx in user_txes:
        print("Block Number: ", tx["blockNumber"])
        tokens_added = get_added_liquidity(tx, tx_fetcher=tx_fetcher)
        print(json.dumps(tokens_added, indent=4))


if __name__ == "__main__":
    main()
