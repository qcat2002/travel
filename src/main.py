import reader
import NSGA
import GA
import os


def main(indicator):
    # 请填写绝对路径
    file_path = ['/Users/zepeng/travel/src/data/eil51-ttp/eil51_n50_uncorr-similar-weights_01.ttp',
                 '/Users/zepeng/travel/src/data/eil51-ttp/eil51_n50_uncorr_01.ttp',
                 '/Users/zepeng/travel/src/data/eil51-ttp/eil51_n50_bounded-strongly-corr_01.ttp']
    # file_path = ['/Users/zepeng/travel/src/data/eil51-ttp/eil51_n150_bounded-strongly-corr_01.ttp',
    #              '/Users/zepeng/travel/src/data/eil51-ttp/eil51_n150_uncorr-similar-weights_01.ttp',
    #              '/Users/zepeng/travel/src/data/eil51-ttp/eil51_n150_uncorr_01.ttp']
    # 请填写 试验次数
    pop_size = 300
    rate = 0.25
    gen = 5000
    m = 30
    trial = 1
    # 调整我
    my_path = file_path[2]
    if indicator:
        print(f"运行 {my_path.split('/')[-1]} ✅")
        information = reader.readttp(my_path)
        while trial <= m:
            print(trial, '次运行')
            algorithm = GA.GA(information,
                              my_path, trial,
                              pop_size,
                              gen,
                              rate)
            algorithm.run()
            trial += 1
    else:
        print(f"运行 {my_path.split('/')[-1]} ✅")
        information = reader.readttp(my_path)
        while trial <= m:
            print(trial, '次运行')
            algorithm = NSGA.NSGA(information,
                                  my_path, trial,
                                  pop_size,
                                  gen,
                                  rate)
            algorithm.run()
            trial += 1

# 0 NSGA / 1 GA
user = input("NSGA 0 / GA 1\n")
main(int(user))
