from datetime import datetime

from web3 import Web3

from get_balances import *
from projects.api.route.tricryptopool_methods import token_contract, price_oracle, calc_withdraw_one_coin
from projects.api.route.utils import get_prices_of_coins

tricrypto_contract = init_contract(TRICRYPTO_CONTRACT_ADDR)


def get_tricrypto_liquidity_positions(user_addr: str):

    user_addr = Web3.toChecksumAddress(user_addr)

    # get total number of LP tokens a user has in the tricrypto pool:
    gauge_bal_convex = get_convex_gauge_bal(user_addr)
    gauge_bal_curve = get_curve_gauge_bal(user_addr)
    gauge_bal = gauge_bal_convex + gauge_bal_curve
    lp_token_bal = get_lp_token_bal(user_addr)
    token_balance_to_calc_on = gauge_bal + lp_token_bal

    time_now = datetime.utcnow().strftime("%Y%m%dT%H%M%S")

    # we calculate position on the following token balance (tokens in gauge + free lp tokens)
    if not token_balance_to_calc_on:
        return {time_now: {}}

    token_prices_coingecko = get_prices_of_coins()

    # calculating position of coins in LP:
    # TODO: currently the following is hardcoded to tricrypto. make it more flexible.
    # this will ensure that the code is prepared for other curve v2
    token_names = ["USDT", "WBTC", "ETH"]
    final_positions = {}
    for i in range(len(token_names)):

        _token = init_contract(token_contract(i, tricrypto_contract=tricrypto_contract))
        _token_decimals = _token.functions.decimals().call()
        _price = 1
        price_from_curve_oracle = _price
        if token_names[i] not in ["USDT"]:
            price_from_curve_oracle = price_oracle(
                token_index=i - 1, tricrypto_contract=tricrypto_contract
            )
            _price = price_from_curve_oracle / 10 ** 18  # 18 digit precision

        _coins = (
            calc_withdraw_one_coin(
                token_balance_to_calc_on, i, tricrypto_contract=tricrypto_contract
            )
            / 10 ** _token_decimals
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

    timestamped_output = {time_now: final_positions}

    return timestamped_output
