from eth_account import Account

acct = Account.create('test')
pk = acct.privateKey
new_pk= pk.hex()
print("privateKey: " + new_pk)
print("address: " + acct.address)