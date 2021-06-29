from brownie import *
from .utils.contract_utils import load_contract


def main():
    whale = "0x57ef012861c4937a76b5d6061be800199a2b9100"

    tri = load_contract("0x80466c64868e1ab14a1ddf27a676c3fcbe638fe5")
    registry = load_contract("0x90e00ace148ca3b23ac1bc8c240c2a7dd9c2d7f5")
    tri_lp = load_contract(registry.get_lp_token(tri))
    tri_gauge = load_contract(registry.get_gauges(tri)[0][0])

    gauge_bal = tri_gauge.balanceOf(whale)
    print(f"Gauge balance {gauge_bal / 10 ** tri_gauge.decimals()}")

    tri_gauge.withdraw(gauge_bal, True, {"from": whale})

    lp_bal = tri_lp.balanceOf(whale)
    print(f"LP balance {lp_bal / 10 ** tri_lp.decimals()}")

    labels = ["usd", "wbtc", "eth"]
    final = []
    for i in range(3):

        _token = load_contract(tri.coins(i))
        _price = 1
        if i > 0:
            _price = tri.price_oracle(i - 1) / 10 ** 18

        tri.remove_liquidity_one_coin(lp_bal, i, 0, {"from": whale})
        _coins = _token.balanceOf(whale) / 10 ** _token.decimals()
        _val = _coins * _price
        final.append(f"{labels[i]}: {_coins} @ ${_price:,.2f} = ${_val:,.2f}")
        chain.undo()

    for f in final:
        print(f)
