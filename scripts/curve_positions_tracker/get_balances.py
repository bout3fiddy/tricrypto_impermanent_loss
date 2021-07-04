from scripts.curve_positions_tracker.utils import init_contract
from scripts.curve_positions_tracker.constants import (
    TRICRYPTO_CURVE_GAUGE_ADDR,
    CONVEX_GETREWARDS_CONTRACT_ADDR,
    TRICRYPTO_LP_TOKEN_ADDR,
)


def get_curve_gauge_bal(address: str):
    contract = init_contract(TRICRYPTO_CURVE_GAUGE_ADDR)
    return contract.functions.balanceOf(address).call()


def get_convex_gauge_bal(address: str):
    contract = init_contract(CONVEX_GETREWARDS_CONTRACT_ADDR)
    return contract.functions.balanceOf(address).call()


def get_lp_token_bal(address: str):
    contract = init_contract(TRICRYPTO_LP_TOKEN_ADDR)
    return contract.functions.balanceOf(address).call()


def main():

    ser_addr = "0x2B99d34a2d45cFBF5B9d5d7595F28fD786AE61c7"
    bal_curve = get_curve_gauge_bal(ser_addr)
    bal_convex = get_convex_gauge_bal(ser_addr)

    print(bal_curve + bal_convex)


if __name__ == "__main__":
    main()
