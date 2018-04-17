# Tutorial Getting Started With Contracts

We rephrase an [article](#https://github.com/EOSIO/eos/wiki/Tutorial-Getting-Started-With-Contracts) from EOSIO wiki.

## Getting Started with Contracts

The purpose of this tutorial is to demonstrate how to setup a local blockchain that can be used to experiment with smart contracts. The first part of this tutorial will focus on:

* Starting a Private Blockchain
* Creating a Wallet
* Loading the Bios Contract
* Creating Accounts

The second part of this tutorial will walk you through creating and deploying your own contracts.

* eosio.token Contract
* Exchange Contract
* Hello World Contract

* This tutorial assumes that you have installed both EOSIO and Tokenika TEOS, therefore, at first import the Tokenika teos python module:
```
import teos
teos.set_verbose(True)
```

## Starting a Private Blockchain

Launch an object `teos.Daemon` that implements interaction with the local EOSIO node. Method `clear` starts this node cleared of any past background:
```
daemon = teos.Daemon()
daemon.clear()
#       nodeos exe file: /mnt/e/Workspaces/EOS/eos/build/programs/nodeos/nodeos
#    genesis state file: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/genesis.json
#        server address: 127.0.0.1:8888
#      config directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir
#      wallet directory: /mnt/e/Workspaces/EOS/eos/build/programs/daemon/data-dir/wallet
#     head block number: 2
#       head block time: 2018-04-10T17:20:54
```
Now, a newly started terminal has the local node running.

## Creating a Wallet

A wallet is a repository of private keys necessary to authorize actions on the blockchain. These keys are stored on disk encrypted using a password generated by the EOSIO node. 

Launch an object `teos.Wallet` that implements a local wallet:
```
wallet = teos.Wallet()
#              password: PW5KLhcjMHeLxiyyrFU8EWncXUHHLNWgw7uxmvKMwMC19jMHR6zWk
#  You need to save this password to be able to lock/unlock the wallet!
```
The wallet name argument is not set here: it defaults to 'default'.

When doing with a real value, this password should be stored in a secure password manager, however, for the purpose of development environment, the password is kept in the wallet object. Therefore, the following instructions make sense:
```
wallet.lock()
wallet.list()
#                wallet: default
wallet.unlock()
>>> wallet.list()          # The starlet marks unlocked:
#                wallet: default *
```

## The Eosio Account and the Bios Contract

You have to owe an valid EOSIO account to be authorized to interact with EOSIO. For tests, you can use the ‘eosio’ account:

```
account_eosio = teos.EosioAccount()
account_eosio.key_private
'5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3'
```
You have to have the private key to your property in your wallet. Perhaps, it is there already:
```
wallet.keys()
#  {
#      "wallet keys": [
#          [
#              "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV",
#              "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
#          ]
#      ]
#  }
```
Indeed, your wallet contains the key to `account_eosio`. I it was not there, you could import it. Now, the following attempt is rejected:
```
wallet.import_key(account_eosio)
ERROR! status code is 500  eosd response is Content-Length: 234  Content-type:
application/json  Server: WebSocket++/0.7.0    {"code":500,"message":"Internal
Service Error","error":{"code":10,"name":"assert_exception","what":"Assert
Exception","details":[{"message":"!\"Key already in wallet\":
","file":"wallet.cpp","line_number":150,"method":"import_key"}]}}
```

Now that you have a wallet with the key for the eosio account loaded, you can set a *default system contract*. For the purposes of development, the default `eosio.bios` contract can be used. This contract enables you to have direct control over the resource allocation of other accounts and to access other privileged API calls. In a public blockchain, this contract will manage the staking and unstaking of tokens to reserve bandwidth for CPU and network activity, and memory for contracts.

The eosio.bios contract can be found in the contracts/eosio.bios folder of your EOSIO source code. The Tokenika teos python is configured to find the proper path.
```
contract_eosio_bios = teos.SetContract(
  account_eosio, "eosio.bios", permission=account_eosio)
#        transaction id: fd45de61bd9f05a570df44faf5fd4db182f6a4f4d4da3b0302735f23645f63d2
``` 
The transaction is authorized and signed by `account_eosio`. 

As the set contract command call has produced the transaction id, the default contract is operational. The result of this transaction setting is that it is generated a transaction with two actions, eosio::setcode and eosio::setabi.

The contract is set to the node in two parts: `code` and `abi` The code defines how the contract runs and the abi describes how to convert between binary and json representations of the arguments. While an abi is technically optional, all of the EOSIO tooling depends upon it for ease of use.

## Creating Accounts

Now that we have setup the basic system contract, we can start to create our own accounts. We will create two accounts, user and tester, and we will need to associate a key with each account. In this example, the same key will be used for both accounts.

To do this we first generate a key for the accounts and import it to the wallet.
```
key_accounts = teos.CreateKey("key_accounts")
#              key name: key_accounts
#           private key: 5JG3gEsowhnQXEYD1z4Vmh2iJMnNrb8oSg9TBVbLFjV7dSuDTrW
#            public key: EOS4vA5JV7zKTJCa83LHrvzbHv4z6G5g6GLXMgSB3JZQu5rDpRueS

wallet.import_key(key_accounts)
```
### Create Two User Accounts

Next we will create two accounts, user and tester, using the key we created and imported above.
```
account_user = teos.Account(account_eosio, "user", key_accounts, key_accounts)
#        transaction id: f94c26662da514fac7027270531e023a6fc8cd4dcd739dc67e...

account_tester = teos.Account(
   account_eosio, "tester", key_accounts, key_accounts)
   #        transaction id: 6eb3e7a64ac2265de855f9c8b0c5677848e8451b4d6dda8...
```
NOTE: The create account subcommand requires two keys, one for the OwnerKey (which in a production environment should be kept highly secure) and one for the ActiveKey. In this tutorial example, the same key is used for both.



## Summary

```
daemon = teos.Daemon()
daemon.clear()
wallet = teos.Wallet()
wallet.lock()
wallet.list()
wallet.unlock()
wallet.list()
account_eosio = teos.EosioAccount()
account_eosio.key_private
wallet.keys()
wallet.import_key(account_eosio)
key_accounts = teos.CreateKey("key_accounts")
wallet.import_key(key_accounts)
account_user = teos.Account(
   account_eosio, "user", key_accounts, key_accounts)
account_tester = teos.Account(
   account_eosio, "tester", key_accounts, key_accounts)
```