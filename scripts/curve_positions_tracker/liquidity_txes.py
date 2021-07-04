import os

from scripts.curve_positions_tracker.constants import (
    CURVE_CRYPTOSWAP_DEPOSIT_ZAP_CONTRACT_ADDR,
)
from scripts.curve_positions_tracker.utils import init_contract, EtherscanContract


def get_added_liquidity(address: str):

    tricrypto_contract = init_contract(CURVE_CRYPTOSWAP_DEPOSIT_ZAP_CONTRACT_ADDR)
    user_transactions = EtherscanContract(
        address=CURVE_CRYPTOSWAP_DEPOSIT_ZAP_CONTRACT_ADDR,
        api_key=os.environ["ETHERSCAN_API_KEY"],
    ).get_tx_with(addr=address.lower())

    total_added_liquidity = []
    for transaction in user_transactions:
        tx_input = transaction["input"]
        decoded_input = tricrypto_contract.decode_function_input(tx_input)
        method_name = decoded_input[0].__dict__["abi"]["name"]

        # only continue if method called was add_liquidity in the contract
        if method_name != "add_liquidity":
            return {}
        tx_amounts = decoded_input[1]["_amounts"]
        added_liquidity_in_tx = {
            "USDT": tx_amounts[0] / 10 ** 7,
            "WBTC": tx_amounts[1] / 10 ** 8,
            "ETH": tx_amounts[2] / 10 ** 18,
        }
        total_added_liquidity.append(
            {
                "block_number": transaction["blockNumber"],
                "tokens_added": added_liquidity_in_tx,
            }
        )

    return total_added_liquidity
