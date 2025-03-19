class CSDN_Middleware:
    def process_request(self, request, spider):
        request.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
        request.headers["Referer"] = "https://blog.csdn.net/{}".format(spider.author_name)
