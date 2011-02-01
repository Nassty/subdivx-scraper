from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector as Selector
from subdivx.items import SubdivxItem
import os
import urllib

class SubdivxSpider(BaseSpider):

    name = "subdivx.com"
    allowed_domains = ["subdivx.com"]
    search_therm = "x-files" 
    start = 0
    end = 60
    start_urls = ["http://subdivx.com/index.php?accion=5&buscar=%s&masdesc=&idusuario=&nick=&oxfecha=&oxcd=&oxdown=&pg=%d" %(search_therm, x) for x in range(start, end)]


    def parse(self, response):
        hxs = Selector(response)
        titles = hxs.select("//div[@id='menu_detalle_buscador']")
        contents = hxs.select("//div[@id='buscador_detalle']")
        items = []
        for i in enumerate(titles):
            title = i[1].select("div/a/text()").extract()
            descr = contents[i[0]].select("div[@id='buscador_detalle_sub']/text()").extract()
            external_file = urllib.urlopen(contents[i[0]].select("div[@id='buscador_detalle_sub_datos']/a[@target='new']/@href").extract()[0])

            self.log("downloading %s (%s)" %(title, external_file.geturl()))

            filename = external_file.geturl().split("/")[-1]
            local_name = "subs/%s.%s" %(title[0],filename.split(".")[-1])
            pos = 1
            while os.path.exists(local_name):
                local_name = "subs/%s-(%i).%s" %(title[0], pos, filename.split(".")[-1])
                pos += 1
            local_file = open(local_name, "wb")
            local_file.write(external_file.read())
            external_file.close()
            local_file.close()

            item = SubdivxItem()
            item["title"] = title
            item["descr"] = descr
            item["file"] = local_name 
            items.append(item)
        return items
