import re

import ef.core.logger as logger
from ef.interface import *


def validate(omittable):
    '''Throw exception if validation fails.
    '''
    err_msg = omittable.err_msg
    if not err_msg:
        return

    if "unknown key" in err_msg:
        raise AccountNotExistError(omittable)
    elif "Error 3080001: Account using more than allotted RAM" in err_msg:
        needs = int(re.search('needs\s(.*)\sbytes\shas', err_msg).group(1))
        has = int(re.search('bytes\shas\s(.*)\sbytes', err_msg).group(1))
        raise LowRamError(needs, needs - has)
    elif "transaction executed locally, but may not be" in err_msg:
        pass
    elif "Wallet already exists" in err_msg:
        raise WalletExistsError(omittable)
    elif "Error 3120002: Nonexistent wallet" in err_msg:
        raise WalletNotExist(
            WalletNotExist.msg_template.format(self.name))
    elif "Invalid wallet password" in err_msg:
        raise InvalidPasswordError(omittable)
    elif "Contract is already running this version of code" in err_msg:
        raise ContractRunning()
    
    #######################################################################
    # NOT ERRORS
    #######################################################################
    
    elif "Error 3120008: Key already exists" in err_msg:
        pass                
    else:
        raise Error(err_msg)
        

class Error(Exception):
    '''Base class for exceptions in EOSFactory.
    '''
    def __init__(self, message, translate=True):
        self.message = logger.error(message, translate)
        Exception.__init__(self, self.message)


class AccountNotExistError(Error):
    '''Account does not exist.

    Attributes:
        account: account argument: an ``Account`` object or account name.
    '''
    def __init__(self, account):
        self.account = account
        Error.__init__(
            self, 
            '''
Account ``{}`` does not exist in the blockchain. It may be created.
'''.format(account_arg(account)), 
            True)
         

class WalletExistsError:
    def __init__(self, wallet):
        self.wallet = wallet
        Error.__init__(
            self, 
            "Wallet ``{}`` already exists.".format(wallet_arg(wallet)), 
            True)


class WalletNotExistError:
    def __init__(self, wallet):
        self.wallet = wallet
        Error.__init__(
            self, 
            "Wallet ``{}`` does not exist.".format(wallet_arg(wallet)), 
            True)


class InvalidPasswordError:
    def __init__(self, wallet):
        self.wallet = wallet
        Error.__init__(
            self, 
            "Invalid password for wallet {}".format(wallet_arg(wallet)), 
            True)


class ContractRunningError:
    def __init__(self):
        Error.__init__(
            self, 
            "Contract is already running this version of code", 
            True)


class LowRamError:
    def __init__(self, needs_byte, deficiency_byte):
        self.needs_kbyte =  needs_byte// 1024 + 1
        self.deficiency_kbyte = deficiency_byte // 1024 + 1
        Error.__init__(
            self, 
            "RAM needed is {}kB, deficiency is {}kB.".format(
            self.needs_kbyte, self.deficiency_kbyte), 
            True)   