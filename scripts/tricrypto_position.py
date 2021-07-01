from datetime import datetime
import pytz

from brownie import *
from .utils.contract_utils import load_contract

from pycoingecko import CoinGeckoAPI


COINGECKO = CoinGeckoAPI()


def get_prices_of_coins():
    eth_price = COINGECKO.get_price(ids="ethereum", vs_currencies="usd")["ethereum"][
        "usd"
    ]
    wbtc_price = COINGECKO.get_price(ids="wrapped-bitcoin", vs_currencies="usd")[
        "wrapped-bitcoin"
    ]["usd"]
    usdt_price = COINGECKO.get_price(ids="tether", vs_currencies="usd")["tether"]["usd"]
    return {"WBTC": wbtc_price, "ETH": eth_price, "USDT": usdt_price}


def get_liquidity_positions(
    user_addr: str,
    curve_liquidity_pool: Contract,
    liquidity_pool_convex_gauge: Contract,
    liquidity_pool_curve_gauge: Contract,
    liquidity_pool_token: Contract,
):

    # get total number of LP tokens a user has in the tricrypto pool:
    gauge_bal_convex = liquidity_pool_convex_gauge.balanceOf(user_addr)
    gauge_bal_curve = liquidity_pool_curve_gauge.balanceOf(user_addr)

    no_lp_tokens_in_gauge = False
    if gauge_bal_convex > 0:
        print(
            f"User has deposited LP tokens to Convex getRewards contract: {liquidity_pool_convex_gauge}."
        )
    elif gauge_bal_curve > 0:
        print(
            f"User has deposited LP tokens to Curve Gauge Contract: {liquidity_pool_curve_gauge}."
        )
    else:
        print("User has not deposited LP tokens to either Convex or Curve Gauges.")
        no_lp_tokens_in_gauge = True

    # get total gauge bal:
    gauge_bal = gauge_bal_convex + gauge_bal_curve
    print(
        f"Gauge balance of User: {gauge_bal / 10 ** liquidity_pool_token.decimals()}."
    )

    lp_token_bal = liquidity_pool_token.balanceOf(user_addr)
    print(
        f"LP token balance of User: {lp_token_bal / 10 ** liquidity_pool_token.decimals()}."
    )

    # we calculate position on the following token balance (tokens in gauge + free lp tokens)
    token_balance_to_calc_on = 0
    if lp_token_bal == 0 and no_lp_tokens_in_gauge:
        print(
            "User has not interacted with Curve contracts at all. "
            "Not calculating tricrypto positions."
        )
        raise
    elif lp_token_bal > 0 and not no_lp_tokens_in_gauge:
        token_balance_to_calc_on = gauge_bal + lp_token_bal
        print(
            f"User has {lp_token_bal} LP tokens that are not staked and "
            f"{gauge_bal} LP tokens that are staked."
        )
    elif lp_token_bal > 0 and no_lp_tokens_in_gauge:
        print("User has not staked any LP tokens in gauge.")
        token_balance_to_calc_on = lp_token_bal
    else:
        print("User has staked all LP tokens in the gauge.")
        token_balance_to_calc_on = gauge_bal

    token_prices_coingecko = get_prices_of_coins()

    # calculating position of coins in LP:
    # TODO: currently the following is hardcoded to tricrypto. make it more flexible.
    # this will ensure that the code is prepared for other curve v2
    token_names = ["USDT", "WBTC", "ETH"]
    final_positions = {}
    for i in range(len(token_names)):

        _token = load_contract(curve_liquidity_pool.coins(i))
        _price = 1
        price_from_curve_oracle = _price
        if token_names[i] not in ["USDT"]:
            price_from_curve_oracle = curve_liquidity_pool.price_oracle(i - 1)
            _price = price_from_curve_oracle / 10 ** 18  # 18 digit precision

        _coins = (
            curve_liquidity_pool.calc_withdraw_one_coin(token_balance_to_calc_on, i)
            / 10 ** _token.decimals()
        )
        _val = _coins * _price
        position_data = {
            "token_contract_address": _token.address,
            "curve_oracle_price_usd": _price,
            "num_tokens": _coins,
            "value_tokens_usd": _val,
            "coingecko_price_usd": token_prices_coingecko[token_names[i]],
        }
        final_positions[token_names[i]] = position_data

    time_now = pytz.utc.localize(datetime.utcnow()).strftime("%Y%m%dT%H%M%S%Z")
    timestamped_output = {time_now: final_positions}

    return timestamped_output


def main():
    import json

    user_addr = "0x0cab140387F737ba642a8cEeeA0D8480668cd92f"

    tricrypto_contract = load_contract("0x80466c64868e1ab14a1ddf27a676c3fcbe638fe5")
    curve_registry = load_contract("0x90e00ace148ca3b23ac1bc8c240c2a7dd9c2d7f5")
    convex_getrewards_contract = load_contract(
        "0x5Edced358e6C0B435D53CC30fbE6f5f0833F404F"
    )
    tricrypto_curve_gauge = load_contract(
        curve_registry.get_gauges(tricrypto_contract)[0][0]
    )
    tricrypto_lp_token_contract = load_contract(
        "0xcA3d75aC011BF5aD07a98d02f18225F9bD9A6BDF"
    )

    positions = get_liquidity_positions(
        user_addr=user_addr,
        curve_liquidity_pool=tricrypto_contract,
        liquidity_pool_convex_gauge=convex_getrewards_contract,
        liquidity_pool_curve_gauge=tricrypto_curve_gauge,
        liquidity_pool_token=tricrypto_lp_token_contract,
    )
    print(json.dumps(positions, indent=4))


if __name__ == "__main__":
    main()