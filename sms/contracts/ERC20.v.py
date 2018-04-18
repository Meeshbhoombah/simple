#
# simple/ERC20.v.py
# The ERC-20 implementation of the Simple token in Vyper.
#


# EVENTS
Transfer: event({_from: indexed(address), _to: indexed(address), _value: uint256})
Approval: event({_owner: indexed(address), _spender: indexed(address), _value: uint256})


name: public(bytes32)
symbol: public(bytes32)
totalSupply: public(uint256)
decimals: public(int128)
balances: int128[address]
allowed: int128[address][address]


@public
def __init__(_name: bytes32, _symbol: bytes32, _decimals: uint256, _initialSupply: uint256):
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals
    self.totalSupply = uint256_mul(_initialSupply, uint256_exp(convert(10, 'uint256'), _decimals))
    self.balances[msg.sender] = convert(self.totalSupply, 'int128')


@public
@constant
def balanceOf(_owner: address) -> uint256:
    return convert(self.balances[_owner], 'uint256')


@public
def transfer(_to: address, _amount: int128(uint256)) -> bool:
    # Send `_value` tokens to `_to` from your account.
    if self.balances[msg.sender] >= _amount and \
       self.balances[_to] + _amount >= self.balances[_to]:

        # Subtract from the sender
        self.balances[msg.sender] -= _amount  
        # Add the same to the recipient
        self.balances[_to] += _amount  
        
        # log transfer event
        log.Transfer(msg.sender, _to, convert(_amount, 'uint256'))

        return True
    else:
        return False


@public
def transferFrom(_from: address, _to: address, _value: int128(uint256)) -> bool:
    # Transfer allowed tokens from a specific account to another.
    if _value <= self.allowed[_from][msg.sender] and \
       _value <= self.balances[_from]:

        self.balances[_from] -= _value  # decrease balance of from address.
        self.allowed[_from][msg.sender] -= _value  # decrease allowance.
        self.balances[_to] += _value  # incease balance of to address.
        log.Transfer(_from, _to, convert(_value, 'uint256'))  # log transfer event.

        return True
    else:
        return False


@public
def approve(_spender: address, _amount: int128(uint256)) -> bool:
# Allow _spender to withdraw from your account, multiple times, up to the _value amount.
# If this function is called again it overwrites the current allowance with _value.
    self.allowed[msg.sender][_spender] = _amount
    log.Approval(msg.sender, _spender, convert(_amount, 'uint256'))
    return True


@public
def allowance(_owner: address, _spender: address) -> uint256:
# Get the allowence an address has to spend anothers' token.
    return convert(self.allowed[_owner][_spender], 'uint256')

