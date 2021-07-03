import unittest
import sys, os, json

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from scripts.utils.etherscan_utils import contract_interactions
from scripts.utils.tricrypto_utils.transaction_parser import get_added_liquidity


class TestAddedLiquidity(unittest.TestCase):
    def test_method_works(self):

        tricrypto_contract = contract_interactions.Contract(
            address="0x331aF2E331bd619DefAa5DAc6c038f53FCF9F785",
            api_key=os.environ["ETHERSCAN_API_KEY"],
        )
        user = "0x2B99d34a2d45cFBF5B9d5d7595F28fD786AE61c7"
        user_transactions = tricrypto_contract.get_tx_with(addr=user.lower())

        for transaction in user_transactions:
            print("Block Number of transaction: ", transaction["blockNumber"])
            tokens_added = get_added_liquidity(transaction)
            assert tokens_added
            print(json.dumps(tokens_added, indent=4))


if __name__ == "__main__":
    unittest.main()
