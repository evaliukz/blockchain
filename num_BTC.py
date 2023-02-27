import math

# Initially, the block reward was 50 BTC, and the reward halves every 210,000 blocks.
# Number the blocks starting at 1 (instead of starting at 0). 
# Thus at Block 1 there were 50 BTC in circulation. At Block 2, 100 BTC etc


def num_BTC(b):
    c = float(0)
    reward = 50

    # n = the rounds of halving
    n = b // 210000

    # m = the remaining number after last halving
    m = b % 210000

    while n > 0:
        c += 210000 * reward
        reward = reward/2
        n = n - 1

    c += m * reward
    return c
