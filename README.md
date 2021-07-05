
# Curve TriCrypto Position Tracker

Tricrypto Position Tracker is a tool that allows a liquidity provider in [Curve's new v2 liquidity pool for US Dollar (Tether; USDT), Wrapped Bitcoin (WBTC) and Ether (ETH)](https://curve.fi/tricrypto) on the Ethereum blockchain. This tool enables monitoring one's liquidity pool positions.

### Available Functionality
1. Get current position in TriCrypto pool.
2. Get deposits.

### Planned
1. API using flask
2. Front-end framework
3. Deployed code in webpage
4. Get value of tokens when deposited.
5. Get Get Withdrawls and value of tokens when withdrawn.

### Holy Grail
*Historical LP positions* (will work with Archival nodes, but not enough experience there yet).

## Installation

There are a few packages to install in order to run the scripts in this repository. The user also needs API keys from [Etherscan](https://etherscan.io/apis) and [Infura](https://infura.io/) in order to query the blockchain for transactions and infer positions.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements in this repository. The user is encouraged to use virtual environments. The instructions here are tested on a 2021 Mac M1 Air.

Requirements: Python >= 3.6.0

```bash
# clone this repo
git clone https://github.com/bout3fiddy/tricrypto_impermanent_loss.git

# create virtual environment first
python3 -m venv venv

# activate virtual environment
source ./venv/bin/activate

# update pip
python3 -m pip install --upgrade pip

# install requirements
pip install -r ./requirements.txt
```

## Usage

Codebase is still under progress. Instructions will be updated soon.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Apache License 2.0](https://github.com/bout3fiddy/tricrypto_impermanent_loss/blob/main/LICENSE)
