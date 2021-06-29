import os

from etherscan.client import Client
from etherscan.accounts import Account


class Contract(Account):
    def __init__(self, address=Client.dao_address, api_key="YourApiKey"):
        Account.__init__(self, address=address, api_key=api_key)
        self.url_dict[self.MODULE] = "account"

    def get_tx_with(
        self, addr: str, start_block: int = 0, end_block=99999999, sort="asc"
    ) -> list(dict):

        self.url_dict[self.ACTION] = "txlist"
        self.url_dict[self.SORT] = sort
        self.url_dict[self.START_BLOCK] = str(start_block)§
        self.url_dict[self.END_BLOCK] = str(end_block)
        self.build_url()
        req = self.connect()
        relevant_txes = []
        for tx in req["result"]:
            if tx["from"] == addr:
                relevant_txes.append(tx)

        return relevant_txes


def main():
    tricrypto_contract = Contract(
        address="0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785",
        api_key=os.environ["ETHERSCAN_API_KEY"],
    )
    user = "0x0cab140387F737ba642a8cEeeA0D8480668cd92f"

    user_txes = tricrypto_contract.get_tx_with(addr=user.lower())



if __name__ == "__main__":
    main()
