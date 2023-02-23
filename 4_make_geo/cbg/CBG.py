import numpy as np
from sklearn.linear_model import LinearRegression
from scipy import optimize, spatial, interpolate

def discard_infeasible(obs):
    """
        检查是否符合 2/3 光速: 200,000 km/s
        记住 RTT 是一个来回
    """
    feasible = np.where(
        obs[1, :] * (1000 * 200) > obs[0, :],
    )
    fobs = obs[:, feasible[0]]
    return fobs

class CBG:
    # obs: 第二列 RTT(ms), 第一列 Distance(km)
    def __init__(self, obs, draw=False):
        # CBG 处理
        obs = discard_infeasible(obs)
        # 排序, RTT, then Distance
        obs = obs[:, np.lexsort((obs[1, :], obs[0, :]))]
        # discard all observations at distance 0, CBG can't make use of them.
        obs = obs[:, obs[0, :] > 0]
        # 每一个相同的 Distance 保留最小的 RTT
        _, uindex = np.unique(obs[0, :], axis=0, return_index=True)
        newobs = obs[:, uindex]

        xs = newobs[0, :] # distance
        ys = newobs[1, :] # rtt

        # 开始线性规划, 转换为 min 问题, 看草稿纸
        A = np.sum(ys) 
        B = -np.sum(xs)
        C = -len(xs)
        cbg_c = [A, B, C]

        cbg_A_ub = np.column_stack((
            np.zeros_like(xs), xs, np.ones_like(xs)
        ))
        cbg_b_ub = ys.tolist()
        cbg_bounds = [(1,1), (1/100000, None), (0, np.amin(ys))]

        fit = optimize.linprog(c=cbg_c,
                               A_ub=cbg_A_ub,
                               b_ub=cbg_b_ub,
                               bounds=cbg_bounds)
        self.FIT = fit
        if draw:
            import matplotlib.pyplot as plt
            m = fit.x[1]
            b = fit.x[2]
            predicts = m * xs + b

            plt.scatter(obs[0, :], obs[1, :])
            plt.plot(xs, predicts, color = 'red')
            plt.show()

    def predict(self, rtt):
        m = self.FIT.x[1]
        b = self.FIT.x[2]

        distance = (rtt - b) / m
        return distance
