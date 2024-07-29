import csv
import numpy as np

class info:
    def __init__(self,
                 problem_name,
                 knapsack_data_type,
                 number_of_city,
                 number_of_item,
                 max_weight,
                 min_speed,
                 max_speed,
                 rent,
                 edge_type,
                 cities,
                 items):
        self.problem_name = problem_name
        self.knapsack_data_type = knapsack_data_type
        self.number_of_city = number_of_city
        self.number_of_item = number_of_item
        self.max_weight = max_weight
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.rent = rent
        self.edge_type = edge_type
        self.cities = cities
        self.items = items
        self.distance_matrix = self.cal()  # a numpy 2d array
        self.items_in_different_city = self.separation()

    def cal(self):
        """
        Aim: Calculate distance between city and city
        :return: a numpy 2d array
        """
        # initialize the numpy 2d array
        distance_matrix = np.zeros((self.number_of_city, self.number_of_city))
        # loop row then col one by one
        for row in range(self.number_of_city):
            for col in range(self.number_of_city):
                # row - start city
                # col - end city
                # capture the coordinate (location) of cities
                x1 = self.cities[row][1]
                y1 = self.cities[row][2]
                x2 = self.cities[col][1]
                y2 = self.cities[col][2]
                # calculate distance (Euclidian Distance)
                distance_matrix[row][col] = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance_matrix

    def separation(self):
        dict = {}
        candidates = [(item[0], item[3]) for item in self.items]
        for city_id in range(self.number_of_city):
            # key ?
            key = city_id
            # value ?
            value = []
            new_candidates = []
            for candidate in candidates:
                # loop check assigned city and save item_index [0~end-1]
                if candidate[1] == city_id:
                    value.append(candidate[0])
                    # value.append(candidate)
                else:
                    # ignore the saved element, saving computational resources
                    new_candidates.append(candidate)
            # update candidates
            candidates = new_candidates
            dict[key] = value
            # print("city id", "item_id list", "[Profit, Weight]")
            # print(key, dict[city_id], [(self.items[item_id][1], self.items[item_id][2]) for item_id in dict[city_id]], '\n')
        return dict



def readttp(path):
    # read head
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        # header information
        problem_name = next(reader)[1]
        knapsack_data_type = next(reader)[0].split(': ')[1]
        number_of_city = int(next(reader)[1])
        number_of_item = int(next(reader)[1])
        max_weight = int(next(reader)[1])
        min_speed = float(next(reader)[1])
        max_speed = float(next(reader)[1])
        rent = float(next(reader)[1])
        edge_type = next(reader)[1]
        # skip line
        next(reader)
        """
        city (node) location information
        [id, x_coordinate, y_coordinate]
        """
        cities = []
        for timer in range(number_of_city):
            city_info = [int(elem) for elem in next(reader)]
            city_info[0] = city_info[0] - 1
            cities.append(city_info)
        # skip line
        next(reader)
        """
        Item:
        Index, Profit, Weight, Assigned Node Number
        """
        # [id, profit, weight, which_city?]
        items = []
        for timer in range(number_of_item):
            item_info = [int(elem) for elem in next(reader)]
            item_info[0] = item_info[0] - 1  # id starts from 0
            item_info[3] = item_info[3] - 1  # id starts from 0
            items.append(item_info)
        myinfo = info(problem_name,
                      knapsack_data_type,
                      number_of_city,
                      number_of_item,
                      max_weight,
                      min_speed,
                      max_speed,
                      rent,
                      edge_type,
                      cities,
                      items)
        return myinfo


if __name__ == '__main__':
    temp_path = 'data/eil51-ttp/eil51_n50_bounded-strongly-corr_01.ttp'
    information = readttp(temp_path)