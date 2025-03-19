import json
import time
from urllib.parse import urlencode

import scrapy
from loguru import logger


class CSDN_Spider(scrapy.Spider):
    name = "csdn"
    allowed_domains = ["csdn.net"]
    start_urls = ["https://blog.csdn.net/MarkAdc"]

    def __init__(self, name, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author_name = name
        self.max_page = int(page)

    def start_requests(self):
        logger.info("开始任务（爬取 {}，最大爬取 {} 页）".format(self.author_name, self.max_page))
        time.sleep(3)
        start_url = "https://blog.csdn.net/{}".format(self.author_name)
        yield scrapy.Request(start_url, callback=self.parse)

    def parse(self, response, *args):
        logger.info("已访问作者主页 {}".format(response.request.url))
        part_url = "https://blog.csdn.net/community/home-api/v1/get-business-list"
        params = {
            "page": "1",
            "size": "20",
            "businessType": "lately",
            "noMore": "false",
            "username": self.author_name
        }
        url = part_url + "?" + urlencode(params)
        yield scrapy.Request(url, self.parse_page, cb_kwargs={"part_url": part_url, "params": params})

    def parse_page(self, response, part_url, params):
        current_page = params["page"]
        data = json.loads(response.text)
        some = data["data"]["list"]
        if not some:
            logger.warning("没有第 {} 页".format(current_page))
            return
        for one in some:
            date = one["formatTime"]
            name = one["title"]
            detail_url = one["url"]
            yield scrapy.Request(detail_url, self.parse_detail, cb_kwargs={"date": date, "name": name})
            print(date, name, detail_url, sep="\n")
            print()
        logger.info("第 {} 页抓取成功".format(params["page"]))

        next_page = int(current_page) + 1
        if next_page > self.max_page:
            logger.warning("超过设定的最大爬取页数了...")
            return
        params["page"] = str(next_page)
        next_url = part_url + "?" + urlencode(params)
        yield scrapy.Request(next_url, self.parse_page, cb_kwargs={"part_url": part_url, "params": params})

    def parse_detail(self, response, date, name):
        logger.success("已访问 {} {}".format(date, name))

    def close(self, reason):
        logger.info("<{}> {}".format(self.name, reason))
