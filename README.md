
# Curve TriCrypto Position Tracker

Tricrypto Position Tracker is a tool that allows a liquidity provider in [Curve's new v2 liquidity pool for US Dollar (Tether; USDT), Wrapped Bitcoin (WBTC) and Ether (ETH)](https://curve.fi/tricrypto) on the Ethereum blockchain. This tool enables monitoring one's liquidity pool positions.

### Available Functionality
1. Get current position in TriCrypto pool.

### Planned
1. Get Deposits and value of tokens when deposited.
2. Get Get Withdrawls and value of tokens when withdrawn.

### Holy Grail
*Historical LP positions*

## Installation

There are a few packages to install in order to run the scripts in this repository. The user also needs API keys from [Etherscan](https://etherscan.io/apis) and [Infura](https://infura.io/) in order to query the blockchain for transactions and infer positions.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements in this repository. The user is encouraged to use virtual environments. The instructions here are tested on a 2021 Mac M1 Air.

Requirements: Python > 3.6.0

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

This should give you most of the tools necessary for running the scripts. There are a few more steps needed to run [eth-brownie](https://eth-brownie.readthedocs.io/en/stable/), which is one of the frameworks used to interact with the Ethereum blockchain (mainnet).

To install eth-brownie, you need the following:
- Node.js > 6.11.5
- npm
- ganache-cli

1. Install Node.js from [here](https://nodejs.org/). To check Node Installation:
```bash
node -v
```
2. Install npm from [here](https://npmjs.com/get-npm). To check version:

```bash
npm -v
```
3. Install [ganache-cli](https://www.trufflesuite.com/ganache)

```bash
npm install -g ganache-cli
ganache-cli --version
```

## Usage

Codebase is still under progress. Instructions will be updated soon.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Apache License 2.0](https://github.com/bout3fiddy/tricrypto_impermanent_loss/blob/main/LICENSE)
