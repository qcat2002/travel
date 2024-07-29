import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec


def display_route(info, route):
    # prepare data
    location_x = [city_info[1] for city_info in info.cities]
    location_y = [city_info[2] for city_info in info.cities]
    # city node
    plt.scatter(location_x, location_y)
    # route
    # city_id had minus 1
    record_x = []
    record_y = []
    for city_id in route:
        city_info = info.cities[city_id]
        record_x.append(city_info[1])
        record_y.append(city_info[2])
    record_x.append(info.cities[0][1])
    record_y.append(info.cities[0][2])
    plt.plot(record_x, record_y, color='red')
    plt.show()

def abc():
    import matplotlib.pyplot as plt
    import numpy as np

    # 假设数据
    cities = np.array([[0, 0], [1, 3], [4, 3], [6, 1], [3, 0], [1, 1]])
    tour = [0, 1, 2, 3, 4, 5, 0]  # 旅行商的路线
    items = [
        {'city': 1, 'weight': 2, 'value': 3, 'selected': 1},
        {'city': 2, 'weight': 3, 'value': 4, 'selected': 1},
        {'city': 3, 'weight': 4, 'value': 8, 'selected': 0},
        {'city': 4, 'weight': 5, 'value': 8, 'selected': 0},
        {'city': 5, 'weight': 9, 'value': 10, 'selected': 1},
    ]
    capacity = 15

    # 计算每个城市的背包状态
    city_weights = np.zeros(len(cities))
    city_values = np.zeros(len(cities))
    for item in items:
        if item['selected']:
            city_weights[item['city']] += item['weight']
            city_values[item['city']] += item['value']

    # 创建图形
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # 绘制旅行商路线图
    ax1.plot(cities[tour, 0], cities[tour, 1], 'o-', label='Tour')
    for i, city in enumerate(cities):
        ax1.text(city[0], city[1], f'City {i}', ha='right')

    ax1.set_title('Traveling Salesman Tour')
    ax1.set_xlabel('X Coordinate')
    ax1.set_ylabel('Y Coordinate')
    ax1.legend()

    # 绘制背包状态图
    index = np.arange(len(cities))
    bar_width = 0.35

    bars1 = ax2.bar(index, city_weights, bar_width, label='Weights')
    bars2 = ax2.bar(index + bar_width, city_values, bar_width, label='Values')

    ax2.set_title('Knapsack Status at Each City')
    ax2.set_xlabel('City Index')
    ax2.set_ylabel('Weight / Value')
    ax2.set_xticks(index + bar_width / 2)
    ax2.set_xticklabels([f'City {i}' for i in range(len(cities))])
    ax2.legend()

    # 添加背包总容量信息
    total_weight = sum(item['weight'] for item in items if item['selected'])
    total_value = sum(item['value'] for item in items if item['selected'])
    ax2.text(0.95, 0.95, f'Total Weight: {total_weight}\nTotal Value: {total_value}\nCapacity: {capacity}',
             transform=ax2.transAxes, ha='right', va='top', bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout()
    plt.show()


def efg():
    import matplotlib.pyplot as plt

    # 假设数据
    class Info:
        def __init__(self, cities):
            self.cities = cities

    class CurrentBest:
        def __init__(self, route):
            self.route = route

    # 假设数据
    cities = {0: (0, 0, 0), 1: (1, 1, 3), 2: (2, 4, 3), 3: (3, 6, 1), 4: (4, 3, 0), 5: (5, 1, 1)}
    node_xs = [0, 1, 4, 6, 3, 1]
    node_ys = [0, 3, 3, 1, 0, 1]
    current_best = CurrentBest([0, 1, 2, 3, 4, 5])
    info = Info(cities)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # 绘制城市
    ax1.scatter(node_xs, node_ys, color='blue', label='City')

    # 准备路线
    route_x = [info.cities[xx][1] for xx in current_best.route] + [info.cities[current_best.route[0]][1]]
    route_y = [info.cities[yy][2] for yy in current_best.route] + [info.cities[current_best.route[0]][2]]

    # 绘制路线
    ax1.plot(route_x, route_y, 'o-', color='red', label='Tour')

    # 添加城市编号标签
    for i, (x, y) in enumerate(zip(node_xs, node_ys)):
        ax1.text(x, y, f'{i}', fontsize=12, ha='right')

    ax1.set_title('Traveling Salesman Tour')
    ax1.set_xlabel('X Coordinate')
    ax1.set_ylabel('Y Coordinate')
    ax1.legend()

    plt.tight_layout()
    plt.show()

def etc():
    # 创建图形对象
    fig = plt.figure(figsize=(22, 10))
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.5, left=0.02)

    # 创建子图
    ax_main = plt.subplot(gs[0])
    ax_main.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])
    # ax_main.legend()

    gs_sub = gridspec.GridSpec(3, 1, height_ratios=[1, 1, 1], hspace=0.13, left=0.4, right=0.98)
    ax_sub1 = plt.subplot(gs_sub[0])
    ax_sub1.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], color='red')


    ax_sub2 = plt.subplot(gs_sub[1])
    ax_sub2.plot([1, 2, 3, 4, 5], [1, 4, 9, 16, 25], color='green')


    ax_sub3 = plt.subplot(gs_sub[2])
    ax_sub3.plot([1, 2, 3, 4, 5], [-1, -4, -9, -16, -25], color='blue')


    plt.show()

if __name__ == '__main__':
    etc()