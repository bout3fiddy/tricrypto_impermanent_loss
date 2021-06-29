import os

query = f"""
https://api.etherscan.io/api?
module=account
&action=txlist
&address=0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
&startblock=0
&endblock=99999999
&sort=asc
&apikey={os.environ["ETHERSCAN_API_KEY"]}
"""
