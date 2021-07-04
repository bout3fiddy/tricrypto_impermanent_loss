def calc_withdraw_one_coin(balance: int, token_index: int, tricrypto_contract):
    return tricrypto_contract.functions.calc_withdraw_one_coin(
        balance, token_index
    ).call()


def price_oracle(token_index: int, tricrypto_contract):
    return tricrypto_contract.functions.price_oracle(token_index).call()


def token_contract(token_index: int, tricrypto_contract):
    return tricrypto_contract.functions.coins(token_index).call()
