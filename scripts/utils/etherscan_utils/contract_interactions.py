from etherscan.client import Client
from etherscan.accounts import Account


class Contract(Account):
    def __init__(self, address=Client.dao_address, api_key="YourApiKey"):
        Account.__init__(self, address=address, api_key=api_key)
        self.url_dict[self.MODULE] = "account"

    def get_tx_with(
        self, addr: str, start_block: int = 0, end_block: int = -1, sort="asc"
    ):

        self.url_dict[self.ACTION] = "txlist"
        self.url_dict[self.SORT] = sort
        self.url_dict[self.START_BLOCK] = str(start_block)
        end_block = str(end_block)
        if int(end_block) == -1:
            end_block = "latest"
        self.url_dict[self.END_BLOCK] = end_block
        self.build_url()
        req = self.connect()
        relevant_txes = []
        for tx in req["result"]:
            if tx["from"] == addr:
                relevant_txes.append(tx)

        return relevant_txes


def main():
    import json
    import os

    tricrypto_contract = Contract(
        address="0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785",
        api_key=os.environ["ETHERSCAN_API_KEY"],
    )
    user = "0xcAf2d3f6c4A375ccEC74eB7eD5c03f5B6cd8876E"

    user_txes = tricrypto_contract.get_tx_with(addr=user.lower())
    for tx in user_txes:
        print(json.dumps(tx, indent=4))


if __name__ == "__main__":
    main()
