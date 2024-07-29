import reader
import GA
import os


def main():
    # 请填写绝对路径
    file_path = '/Users/zepeng/travel/src/data/eil51-ttp/eil51_n150_bounded-strongly-corr_01.ttp'
    # 请填写 试验次数
    m = 30
    trial = 1
    while trial <= m:
        information = reader.readttp(file_path)
        algorithm = GA.GA(information,
                          file_path, trial,
                          200,
                          10000,
                          0.2)
        algorithm.run()
        trial += 1


main()
