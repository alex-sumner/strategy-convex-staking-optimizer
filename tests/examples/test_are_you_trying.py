from brownie import *
from helpers.constants import MaxUint256


def test_are_you_trying(deployer, sett, strategy, want):
    """
    Verifies that you set up the Strategy properly
    """
    # Setup
    startingBalance = want.balanceOf(deployer)

    depositAmount = startingBalance // 2
    assert startingBalance >= depositAmount
    assert startingBalance >= 0
    # End Setup

    # Deposit
    assert want.balanceOf(sett) == 0

    want.approve(sett, MaxUint256, {"from": deployer})
    sett.deposit(depositAmount, {"from": deployer})

    available = sett.available()
    assert available > 0

    sett.earn({"from": deployer})

    chain.sleep(10000 * 13)  # Mine so we get some interest

    ## TEST 1: Does the want get used in any way?
    assert want.balanceOf(sett) == depositAmount - available

    # Did the strategy do something with the asset?
    assert want.balanceOf(strategy) < available

    # Use this if it should invest all
    # assert want.balanceOf(strategy) == 0

    # Change to this if the strat is supposed to hodl and do nothing
    # assert strategy.balanceOf(want) = depositAmount

    ## TEST 2: How much gas does the harvest use?
    balanceBefore = strategy.balanceOf()

    harvest = strategy.harvest({"from": deployer})
    gasUsed = harvest.gas_used
    for delay in [1200, 85000, 20000, 3600, 86400, 230000, 34567, 92611, 180234]:
        chain.sleep(delay)
        harvest = strategy.harvest({"from": deployer})
        gasUsed += harvest.gas_used

    balanceAfter = strategy.balanceOf()
    assert balanceAfter >= balanceBefore
    balanceIncrease = balanceAfter - balanceBefore
    print("gas used: ", gasUsed, ", balance increase ", balanceIncrease)
    assert False
