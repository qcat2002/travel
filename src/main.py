import reader
import GA
import os


def main():
    # 请填写绝对路径
    # file_path = ['/Users/zepeng/travel/src/data/eil51-ttp/eil51_n50_uncorr-similar-weights_01.ttp',
    #              '/Users/zepeng/travel/src/data/eil51-ttp/eil51_n50_uncorr_01.ttp',
    #              '/Users/zepeng/travel/src/data/eil51-ttp/eil51_n50_bounded-strongly-corr_01.ttp']
    file_path = ['/Users/zepeng/travel/src/data/eil51-ttp/eil51_n150_bounded-strongly-corr_01.ttp',
                 '/Users/zepeng/travel/src/data/eil51-ttp/eil51_n150_uncorr-similar-weights_01.ttp',
                 '/Users/zepeng/travel/src/data/eil51-ttp/eil51_n150_uncorr_01.ttp']
    # 请填写 试验次数
    m = 30
    trial = 1
    # 调整我
    my_path = file_path[1]
    print(f"运行 {my_path.split('/')[-1]} ✅")
    while trial <= m:
        information = reader.readttp(my_path)
        algorithm = GA.GA(information,
                          my_path, trial,
                          200,
                          10000,
                          0.15)
        algorithm.run()
        trial += 1


main()
