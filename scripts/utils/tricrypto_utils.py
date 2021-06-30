from etherscan.proxies import Proxies


def get_erc20_token_transfers(tx_hash: str, tx_fetcher: Proxies):

    tx_receipt = tx_fetcher.get_transaction_receipt(tx_hash=tx_hash)

    return tx_receipt


def main():
    from .etherscan_utils.contract_interactions import Contract
    import os

    tx_fetcher = Proxies(api_key=os.environ["ETHERSCAN_API_KEY"])

    tricrypto_contract = Contract(
        address="0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785",
        api_key=os.environ["ETHERSCAN_API_KEY"],
    )
    user = "0xcAf2d3f6c4A375ccEC74eB7eD5c03f5B6cd8876E"

    user_txes = tricrypto_contract.get_tx_with(addr=user.lower())
    for tx in user_txes:
        tokens_added = get_erc20_token_transfers(tx["hash"], tx_fetcher=tx_fetcher)


if __name__ == "__main__":
    main()
