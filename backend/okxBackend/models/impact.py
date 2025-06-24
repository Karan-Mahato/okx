import numpy as np

"""
sigma: Volatility estimate (e.g., 5%)
eta: Temporary impact coefficient
gamma: Permanent impact coefficient
"""

class AlmgrenChrissModel:
    def __init__(self, sigma=0.05, eta=0.01, gamma=0.1):
        self.sigma = sigma
        self.eta = eta
        self.gamma = gamma

    def estimate_impact(self, quantity, price, time_horizon=1, liquidity=1000000):
        """
        Parameters:
        - quantity: Order size in USD
        - price: Current mid price
        - time_horizon: Execution period in seconds (shorter = more aggressive)
        - liquidity: Approximate market depth (adjustable)

        Returns:
        - Estimated market impact in USD
        """
        x = quantity / price  # convert to base asset amount
        v = liquidity / time_horizon  # volume participation rate

        temporary_impact = self.eta * (x / v)
        permanent_impact = self.gamma * (x / liquidity)

        impact = price * (temporary_impact + permanent_impact)
        return round(impact, 6)
