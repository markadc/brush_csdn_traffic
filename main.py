import argparse
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--times", type=int, default=1, help="Scrapy 运行次数（默认 1 次）")
parser.add_argument("-k", "--keep", action="store_true", help="Scrapy 是否常驻（默认否）")
parser.add_argument("-i", "--interval", type=int, default=60, help="Scrapy 每运行一次的间隔（默认 60 秒）")
parser.add_argument("-n", "--name", default="markadc", help="爬取的作者名称")
parser.add_argument("-p", "--page", type=int, default=2, help="爬取的最大页数")
args = parser.parse_args().__dict__
t, k, i, n, p = args["times"], args["keep"], args["interval"], args["name"], args["page"]


def job():
    subprocess.run("scrapy crawl csdn -a name={} -a page={}".format(n, p).split())


def main():
    global i

    if k is True:
        n = 0
        while True:
            job()
            print("第 {} 轮结束...{} 秒后继续启动爬虫".format(n + 1, i))
            time.sleep(i)

    for n in range(t):
        job()
        print("第 {} 轮结束...".format(n + 1))
        if n != t - 1:
            print("{} 秒后继续启动爬虫".format(i))
            time.sleep(i)

    print(args)


if __name__ == "__main__":
    main()
