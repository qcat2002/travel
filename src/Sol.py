class Ind:
    def __init__(self, route, kp):
        self.route = route
        self.kp = kp
        self.profit = -1
        self.payout = -1
        self.weight = -1
        self.time = -1
        self.fitness = -1

    def copy_me(self):
        new_ind = Ind(self.route, self.kp)
        new_ind.profit = self.profit
        new_ind.payout = self.payout
        new_ind.weight = self.weight
        new_ind.time = self.time
        new_ind.fitness = self.fitness
        return new_ind

    def checker(self, info):
        weight_counter = 0
        profit_counter = 0
        for index in range(len(self.kp)):
            # collect item information
            # Index, Profit, Weight, Assigned Node Number
            item_info = info.items[index]
            # 0 or 1
            if self.kp[index]:
                # picked, then add more weight
                profit_counter += item_info[1]  # 1 - profit
                weight_counter += item_info[2]  # 2 - weight
        # record recent data
        self.profit = profit_counter
        self.weight = weight_counter
        if weight_counter > info.max_weight:
            # require repair
            # checker (function) halting
            return True
        else:
            return False

    def repair(self, info):
        """
        修复思路：
        根据物品拾取计划，利润率排序，最低的被优先抛弃
        抛弃重量 >= 超重重量， ok！
        """
        # search and record the index of picked items
        # 0, 8, 9, ... 指针
        item_indices = [index for index in range(len(self.kp)) if self.kp[index]]
        ratios = []
        for index in item_indices:
            # [index, profit, weight, assigned city]
            item_info = info.items[index]
            # ratio = profit / weight
            ratios.append((index, item_info[1] / item_info[2]))
        # ratio prepared but not sort!
        # sort picked items with index by ratio from high to low
        ratios = sorted(ratios, key=lambda x: x[1], reverse=True)
        # among to weight exceeding the maximum (must be positive)
        extra_weight = self.weight - info.max_weight
        throw = 0
        throw_index = []
        # print(self.kp)
        while throw < extra_weight:
            # get (pop) the last element in the list
            elem = ratios.pop()
            # (index, specific ratio)
            selected_index = elem[0]
            throw_index.append(selected_index)
            throw += info.items[selected_index][2]
            self.kp[selected_index] = 0

    def evaluate(self, info):
        """
        if True:
            then repair
        else:
            then continue evaluating
        """
        if self.checker(info):
            # repair
            # print("我修复！")
            self.repair(info)
        # start to evaluate a legal solution
        # calculate the profit and cost by route
        current_weight = 0
        current_profit = 0
        time = 0
        coefficient = (info.max_speed - info.min_speed) / info.max_weight
        for timer in range(info.number_of_city):
            first = self.route[timer]
            second = self.route[(timer + 1) % info.number_of_city]
            # distance
            distance = float(info.distance_matrix[first][second])
            # calculate weight at start city
            city_id = info.cities[first][0]
            # [indices] list of item index
            items_indices_at_this_city = info.items_in_different_city[city_id]
            # then searching the item information by their id
            for index in items_indices_at_this_city:
                if self.kp[index]:
                    item_info = info.items[index]
                    current_profit += item_info[1]
                    current_weight += item_info[2]
            # speed
            speed = info.max_speed - (coefficient * current_weight)
            # test case, please comment it after testing
            if speed < info.min_speed:
                speed = info.min_speed
            time += distance / speed
        # end statistic
        self.profit = current_profit
        self.weight = current_weight
        self.time = time
        self.payout = info.rent * time
        self.fitness = current_profit - self.payout



