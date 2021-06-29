from brownie import *
from .utils.contract_utils import load_contract


def main():
    user_addr = "0x57ef012861c4937a76b5d6061be800199a2b9100"

    tricrypto_contract = load_contract("0x80466c64868e1ab14a1ddf27a676c3fcbe638fe5")
    convex_getrewards_contract = load_contract(
        "0x5Edced358e6C0B435D53CC30fbE6f5f0833F404F"
    )
    tricrypto_lp_token_contract = load_contract(
        "0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF"
    )

    gauge_bal = convex_getrewards_contract.balanceOf(user_addr)
    print(
        f"Gauge balance of User: {gauge_bal / 10 ** tricrypto_lp_token_contract.decimals()}."
    )

    if gauge_bal == 0:
        print(
            f"User does not have any deposits with the TriCrypto "
            f"GetRewards Contract {convex_getrewards_contract}."
        )
        raise

    labels = ["usd", "wbtc", "eth"]
    final = []
    for i in range(3):

        _token = load_contract(tricrypto_contract.coins(i))
        _price = 1
        if i > 0:
            _price = tricrypto_contract.price_oracle(i - 1) / 10 ** 18

        _coins = (
            tricrypto_contract.calc_withdraw_one_coin(gauge_bal, i)
            / 10 ** _token.decimals()
        )

        _val = _coins * _price
        final.append(f"{labels[i]}: {_coins} @ ${_price:,.2f} = ${_val:,.2f}")

    print("Balance Summary:")
    for f in final:
        print(f)