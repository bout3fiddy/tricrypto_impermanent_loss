import os

from etherscan.contracts import Contract
from web3 import Web3

from etherscan.client import Client
from etherscan.accounts import Account
from pycoingecko import CoinGeckoAPI

WEB3 = Web3(
    Web3.HTTPProvider(
        f"https://mainnet.infura.io/v3/{os.environ['WEB3_INFURA_PROJECT_ID']}"
    )
)
COINGECKO = CoinGeckoAPI()


def init_contract(address: str):

    address = Web3.toChecksumAddress(address)
    contract_abi = Contract(
        address=address, api_key=os.environ["ETHERSCAN_API_KEY"]
    ).get_abi()
    contract = WEB3.eth.contract(address=address, abi=contract_abi)
    return contract


def get_prices_of_coins():
    eth_price = COINGECKO.get_price(ids="ethereum", vs_currencies="usd")["ethereum"][
        "usd"
    ]
    wbtc_price = COINGECKO.get_price(ids="wrapped-bitcoin", vs_currencies="usd")[
        "wrapped-bitcoin"
    ]["usd"]
    usdt_price = COINGECKO.get_price(ids="tether", vs_currencies="usd")["tether"]["usd"]
    return {"WBTC": wbtc_price, "ETH": eth_price, "USDT": usdt_price}


class EtherscanContract(Account):
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
