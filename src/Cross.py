import EAX
import random


def twoPointCross(kp1, kp2):
    start = random.randint(0, len(kp1) - 1)
    end = random.randint(start, len(kp2) - 1)
    kp1 = kp1[0:start] + kp2[start:end] + kp1[end:]
    kp2 = kp2[0:start] + kp1[start:end] + kp2[end:]
    return kp1, kp2


def cross_me(parent1, parent2):
    parent1_route = parent1.route[:]
    parent2_route = parent2.route[:]
    # cross route
    child1_route = EAX.crossover_EAX(parent1_route, parent2_route)
    child2_route = EAX.crossover_EAX(parent1_route, parent2_route)

    parent1_kp = parent1.kp[:]
    parent2_kp = parent2.kp[:]
    # cross kp
    child1_kp, child2_kp = twoPointCross(parent1_kp, parent2_kp)
    return child1_route, child2_route, child1_kp, child2_kp
