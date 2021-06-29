from brownie import Contract, ZERO_ADDRESS


def load_contract(c):
    if c == ZERO_ADDRESS:
        return None
    try:
        return Contract(c)
    except:
        return Contract.from_explorer(c)
