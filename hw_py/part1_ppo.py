import numpy as np
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.check_ppo import (
    check_monte_carlo,
    check_td_residual,
    check_gae,
    check_policy_loss,
    check_value_loss,
)

# Monte Carlo Advantage
def monte_carlo_advantage(rewards: np.ndarray, values: np.ndarray, gamma: float):
    """
    Monte Carlo advantage estimation.

    Args:
        rewards (np.ndarray): sequence of rewards with shape (T,).
        values (np.ndarray): sequence of estimated state values with shape (T+1,).
        gamma (float): discount factor.

    Returns:
        advantages: (np.array) Gt - V(s)
    """
    # TODO: your code here
    Gt = []
    g = 0.0
    for r in rewards[::-1]:
        g = r + gamma * g
        Gt.append(g)
    Gt = np.array(Gt[::-1])
    advantages = Gt - values[:-1]
    return advantages

def td_residual_advantage(rewards: np.ndarray, values: np.ndarray, gamma: float):
    """
    TD(0) residual advantage estimation (one-step TD error).

    Args:
        rewards: list or np.array of rewards with shape (T,).
        values: list or np.array of values  with shape (T+1,).
        gamma: discount factor.

    Returns:
        advantages: (np.array) δ_t = r_t + γ * V(s_{t+1}) - V(s_t)
    """
    # TODO: your code here
    T = len(rewards)
    advantages = np.zeros(T)
    for t in range(T):
        advantages[t] = rewards[t] + gamma * values[t+1] - values[t]
    return advantages


def generalized_advantage_estimation(rewards, values, gamma, lam):
    """
    Generalized Advantage Estimation (GAE).

    Args:
        rewards: list or np.array of rewards.
        values: list or np.array of values (length = len(rewards) + 1).
        gamma: discount factor.
        lam: GAE lambda parameter (between 0 and 1).
               λ=0: reduces to TD(0) (high bias, low variance).
               λ=1: reduces to Monte Carlo (low bias, high variance).

    Returns:
        advantages: (np.array) GAE advantages
    """
    # TODO: your code here
    td_delta = td_residual_advantage(rewards, values, gamma)
    advantages = []
    a = 0.0
    for td in td_delta[::-1]:
        a = td + gamma * lam * a
        advantages.append(a)
    advantages = np.array(advantages[::-1])
    return advantages


def compute_policy_loss(ratio, adv, dist_entropy, epsilon, entropy_weight):
    """
    Compute the policy (actor) loss for PPO using NumPy.

    Args:
        ratio (np.ndarray): Probability ratios between new and old policies.
        adv (np.ndarray): Advantage estimates.
        dist_entropy (float): Precomputed mean entropy of the new policy distribution.
        epsilon (float): PPO clip range.
        entropy_weight (float): Entropy bonus weight.

    Returns:
        float: The computed policy loss (scalar).
    """
    # TODO: your code here
    surr1 = ratio * adv
    surr2 = np.clip(ratio, 1-epsilon, 1+epsilon) * adv
    policy_loss = -np.mean(np.minimum(surr1, surr2)) - entropy_weight * dist_entropy
    return policy_loss


def compute_value_loss(values, returns):
    """
    Compute the value loss for PPO using NumPy. The loss should be Mean Squared Error (MSE) between predicted values and target returns.

    Args:
        values (np.ndarray): Predicted state values.
        returns (np.ndarray): Target returns.

    Returns:
        float: The computed value loss (scalar).
    """
    # TODO: your code here
    return np.mean((values - returns)**2)

# check correctness
check_monte_carlo(monte_carlo_advantage)
check_td_residual(td_residual_advantage)
check_gae(generalized_advantage_estimation)
check_policy_loss(compute_policy_loss)
check_value_loss(compute_value_loss)
