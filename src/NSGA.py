import random
import Sol
import Cross
import Mutate
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.gridspec as gridspec
import csv
import os

class NSGA:
    def __init__(self, info, ttp_path, trial, population_size, generations, mutate_rate):
        self.info = info
        self.ttp_path = ttp_path
        self.trial = trial
        self.save_folder = self.ttp_path.split('.ttp')[0] + f'/NSGA/trial{trial}/'
        self.population_size = population_size
        self.generations = generations
        self.mutate_rate = mutate_rate
        self.good_solutions = []
        self.route_mutation = 0.55
        self.kp_mutation = 0.7
        self.city_weights = []
        self.city_profits = []
        self.node_xs = [city_info[1] for city_info in info.cities]
        self.node_ys = [city_info[2] for city_info in info.cities]

    def writer_log(self):
        file_name = f"Best Solutions Within_{self.generations}.csv"
        file_path = self.save_folder + file_name
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            for ind_each_gen in self.good_solutions:
                information_row = ['fitness', ind_each_gen.fitness,
                                   'time', ind_each_gen.time,
                                   'weight', ind_each_gen.weight,
                                   'profit', ind_each_gen.profit]
                writer.writerow(information_row)
                writer.writerow(ind_each_gen.route)
                writer.writerow(ind_each_gen.kp)

    def writer_result(self, pop):
        file_name = f"A-Results.csv"
        file_path = self.save_folder + file_name
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            count = len(pop)
            if count > 100:
                count = 100
            writer.writerow(['Generation: ', self.generations])
            writer.writerow(['Population Size: ', count])
            writer.writerow(['Mutation Rate: ', self.mutate_rate])
            writer.writerow(['TSP Mutation Rate: ', self.route_mutation])
            writer.writerow(['KP Mutation Rate', self.kp_mutation])
            for ind in pop[:count]:
                information_row = ['fitness', ind.fitness,
                                   'time', ind.time,
                                   'weight', ind.weight,
                                   'profit', ind.profit]
                writer.writerow(information_row)
                writer.writerow(ind.route)
                writer.writerow(ind.kp)

    def show_pareto(self, gen, pop, elite):
        x = [ind.profit for ind in pop]
        y = [ind.time for ind in pop]
        plt.scatter(x,y)
        plt.scatter(elite.profit, elite.time, color='black')
        plt.title(f"Generation-{gen}_({round(elite.fitness)})")
        if not os.path.exists(self.save_folder + "/pareto front"):
            os.makedirs(self.save_folder + "/pareto front")
        plt.savefig(self.save_folder + "/pareto front/" + f'Gen{gen}.png', dpi=300)
        plt.close()

    def show_route(self, gen):
        """
        Aim: The function is usd to display the route of current best solution.
        :return: Null
        """
        font_properties = FontProperties(weight='bold')
        # 创建图形
        # 创建图形对象
        fig = plt.figure(figsize=(24, 10))
        gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.5, left=0.02)
        # get the best solution recently in the history list
        current_best = self.good_solutions[-1]
        # draw diagram
        # ax1
        ax_main = plt.subplot(gs[0])
        p_xs = self.node_xs
        p_ys = self.node_ys
        ax_main.scatter(p_xs, p_ys, color='#6495ED', label="City")
        # prepare route
        route_x = [self.info.cities[xx][1] for xx in current_best.route] + [self.info.cities[0][1]]
        route_y = [self.info.cities[yy][2] for yy in current_best.route] + [self.info.cities[0][2]]
        ax_main.plot(route_x, route_y, '-', color=(1, 0, 0.15), label='Tour', linewidth=1)
        ax_main.set_xlabel('X Coordinate', fontweight='bold')
        ax_main.set_ylabel('Y Coordinate', fontweight='bold')
        # 添加城市编号标签
        for i, (x, y) in enumerate(zip(self.node_xs, self.node_ys)):
            ax_main.text(x, y, f'{i+1}', fontsize=9, ha='center')
        # 加粗刻度数字
        ax_main.tick_params(axis='both', which='both', labelsize=12)  # 设置刻度标签的字体大小
        for label in ax_main.get_xticklabels() + ax_main.get_yticklabels():
            label.set_fontweight('bold')  # 设置刻度标签的字体加粗
        ax_main.legend(prop=font_properties)
        if gen != 1:
            last_best = self.good_solutions[-100]
            ax_main.set_title(f"Generation-{gen}_{self.info.problem_name}_{self.info.number_of_item}_({round(current_best.fitness)})(+{round(current_best.fitness-last_best.fitness)})_Time-{round(current_best.time)}",
                              fontweight='bold')
        else:
            ax_main.set_title(f"Generation-{gen}_{self.info.problem_name}_{self.info.number_of_item}_({round(current_best.fitness)})(N/A)_Time-{round(current_best.time)}",
                              fontweight='bold')
        # ax2
        city_label = [f"{city_id+1}" for city_id in range(self.info.number_of_city)]
        # print(city_label)
        city_id = 0
        # 单个条形的城市数量
        numb = 48
        number_of_graph = self.info.number_of_city // numb
        if (number_of_graph * numb) < self.info.number_of_city:
            number_of_graph += 1
        if number_of_graph == 1:
            number_of_graph = 3
        gs_sub = gridspec.GridSpec(number_of_graph, 1, height_ratios=[1 for _ in range(number_of_graph)], hspace=0.25, left=0.38, right=0.99)
        ax_title = fig.add_subplot(gs_sub[0])
        ax_title.set_title(f"({self.info.knapsack_data_type}) Picked and NOT-picked Items (X-Ticks = City ID)_Weight-{round(current_best.weight)}_Profit-{round(current_best.profit)}",
                           fontsize=12, fontweight='bold')
        # print(current_best.route)
        for timer in range(number_of_graph):
            ax_sub = plt.subplot(gs_sub[timer])
            picked_xs = []
            picked_ys = []
            picked_id = []
            unpicked_xs = []
            unpicked_ys = []
            unpicked_id = []
            consume = numb
            if (self.info.number_of_city - city_id) <= consume:
                consume = self.info.number_of_city - city_id
            # 设置 x 轴刻度和刻度标签
            x = list(range(city_id, city_id+consume))
            ax_sub.set_xticks(x)
            used_city_ID = []
            for inner_t in range(consume):
                searcher = current_best.route[city_id]
                # get all possible items in this city
                used_city_ID.append(city_label[searcher])
                indices = self.info.items_in_different_city[searcher]
                # get pick up information
                y_height = 0
                for index in indices:
                    if current_best.kp[index]:
                        picked_xs.append(city_id)
                        picked_ys.append(y_height)
                        picked_id.append(index+1)
                    else:
                        unpicked_xs.append(city_id)
                        unpicked_ys.append(y_height)
                        unpicked_id.append(index+1)
                    y_height += 0.1
                city_id += 1
            ax_sub.set_xticklabels(used_city_ID)
            ax_sub.scatter(picked_xs, picked_ys, color='red', label="Picked", marker='s')
            ax_sub.scatter(unpicked_xs, unpicked_ys, color='black', label="Otherwise", facecolors='none')
            ax_sub.get_yaxis().set_visible(False)
            # for i, txt in enumerate(picked_id):
            #     plt.annotate(txt, (picked_xs[i], picked_ys[i]), textcoords="offset points", xytext=(0, 3.5),
            #                  ha='center', color='red')
            # for i, txt in enumerate(unpicked_id):
            #     plt.annotate(txt, (unpicked_xs[i], unpicked_ys[i]), textcoords="offset points", xytext=(0, 3.5),
            #                  ha='center', color='black')
            ax_sub.legend()
            ax_sub.grid(axis='x')
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        plt.savefig(self.save_folder + f'Gen{gen}.png', dpi=300)
        plt.close()

    def non_dominated_sort(self, population):
        fronts = [[]]
        domination_count = {}
        dominated_solutions = {}
        rank = {}

        for p in population:
            domination_count[p] = 0
            dominated_solutions[p] = []
            for q in population:
                if self.dominates(p, q):
                    dominated_solutions[p].append(q)
                elif self.dominates(q, p):
                    domination_count[p] += 1
            if domination_count[p] == 0:
                rank[p] = 0
                fronts[0].append(p)

        i = 0
        while len(fronts[i]) > 0:
            next_front = []
            for p in fronts[i]:
                for q in dominated_solutions[p]:
                    domination_count[q] -= 1
                    if domination_count[q] == 0:
                        rank[q] = i + 1
                        next_front.append(q)
            i += 1
            fronts.append(next_front)

        fronts.pop()
        return fronts

    def dominates(self, individual1, individual2):
        return (individual1.profit >= individual2.profit and individual1.time <= individual2.time) and \
            (individual1.profit > individual2.profit or individual1.time < individual2.time)

    def calculate_crowding_distance(self, front):
        distance = {individual: 0 for individual in front}
        num_individuals = len(front)

        if num_individuals == 0:
            return distance

        objectives = ['profit', 'time']
        for obj in objectives:
            front.sort(key=lambda x: getattr(x, obj))
            distance[front[0]] = float('inf')
            distance[front[-1]] = float('inf')
            obj_min = getattr(front[0], obj)
            obj_max = getattr(front[-1], obj)
            for i in range(1, num_individuals - 1):
                if obj_max - obj_min == 0:
                    distance[front[i]] += 0
                else:
                    distance[front[i]] += (getattr(front[i + 1], obj) - getattr(front[i - 1], obj)) / (
                                obj_max - obj_min)

        return distance

    def run(self):
        """
        这是 NSGA 的算法方法
        """
        # Initialization
        pop = []
        original_route = [city_info[0] for city_info in self.info.cities[1:]]
        for timer in range(self.population_size):
            # randomized route
            new_route = original_route[:]
            random.shuffle(new_route)
            route = [0] + new_route
            # empty knapsack
            kp = [0] * len(self.info.items)
            # append to pop
            initial_solution = Sol.Ind(route, kp)
            initial_solution.evaluate(self.info)
            # print(timer + 1, f'Fitness：{initial_solution.fitness}')
            pop.append(initial_solution)
        print('初始化 100 个 个体-完成✅')
        # evolution
        for gen in range(self.generations):
            parents = []
            offspring = []
            vacancy = 0
            # tournament
            while vacancy < self.population_size:
                vacancy += 1
                candidate = random.sample(pop, 2)
                if candidate[0].fitness > candidate[1].fitness:
                    parents.append(candidate[0])
                else:
                    parents.append(candidate[1])
                # print([ind.fitness for ind in parents])
            remain = vacancy
            while remain > 0:
                parent1 = parents.pop()
                parent2 = parents.pop()
                # cross
                cr1, cr2, ckp1, ckp2 = Cross.cross_me(parent1, parent2)
                # mutate
                cr1, cr2, ckp1, ckp2 = Mutate.mutate_me(cr1, cr2, ckp1, ckp2, self.route_mutation, self.kp_mutation)
                child1 = Sol.Ind(cr1, ckp1)
                child2 = Sol.Ind(cr2, ckp2)
                child1.evaluate(self.info)
                child2.evaluate(self.info)
                offspring.extend([child1, child2])
                remain -= 2
            big_pop = pop + offspring
            # Non Dominating Selection
            fronts = self.non_dominated_sort(big_pop)
            selected = []
            for front in fronts:
                sorted_front = self.calculate_crowding_distance(front)
                if len(selected) > self.population_size:
                    break
                selected.extend(sorted_front.keys())
            selected = selected[:self.population_size]
            pop = selected
            # find elite
            elite = max(selected, key=lambda x: x.fitness)
            self.good_solutions.append(elite)
            if (gen+1) % 100 == 0 or gen == 0:
                print(gen+1, elite.fitness)
                self.show_route(gen+1)
                self.show_pareto(gen+1, pop, elite)