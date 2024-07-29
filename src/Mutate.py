import random


def two_opt(route, tsp_rate):
    if random.random() < tsp_rate:
        start = random.randint(0, len(route) - 1)
        end = random.randint(start, len(route) - 1)
        return route[0:start] + route[start:end][::-1] + route[end:]
    return route


def bitflip(kp, kp_rate):
    if random.random() < kp_rate:
        new_kp = []
        for bit in kp:
            if random.random() < 0.5:
                new_kp.append((bit + 1) % 2)
            else:
                new_kp.append(bit)
        return new_kp
    return kp


def mutate_me(cr1, cr2, ckp1, ckp2, tsp_rate, kp_rate):
    cr1 = [0] + two_opt(cr1[1:], tsp_rate)
    cr2 = [0] + two_opt(cr2[1:], tsp_rate)
    ckp1 = bitflip(ckp1, kp_rate)
    ckp2 = bitflip(ckp2, kp_rate)
    return cr1, cr2, ckp1, ckp2
