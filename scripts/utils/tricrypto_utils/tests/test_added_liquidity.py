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