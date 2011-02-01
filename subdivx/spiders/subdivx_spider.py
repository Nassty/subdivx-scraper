from scrapy.spider import BaseSpider
from scrapy.conf import settings
from scrapy.selector import HtmlXPathSelector as Selector
from subdivx.items import SubdivxItem
from scrapy.http import Request
import os
import sys
import urllib

class SubdivxSpider(BaseSpider):

    name = "subdivx.com"
    allowed_domains = ["subdivx.com"]
    search_therm = settings.get("serie", "x-files") 
    start = 0
    end = 60
    start_urls = ["http://subdivx.com/index.php?buscar=%s&accion=5&masdesc=&subtitulos=1&realiza_b=1" %search_therm]

    def parse_subtitle(self, response, item):
        filename = response.url.split("/")[-1]
        local_name = "subs/%s.%s" %(item["title"],filename.split(".")[-1])
        pos = 1
        while os.path.exists(local_name):
            local_name = "subs/%s-(%i).%s" %(item["title"], pos, filename.split(".")[-1])
            pos += 1
        local_file = open(local_name, "wb")
        local_file.write(response.body)
        local_file.close()
        item["file"] = local_name
        return item

    def parse(self, response):
        hxs = Selector(response)
        titles = hxs.select("//div[@id='menu_detalle_buscador']")
        contents = hxs.select("//div[@id='buscador_detalle']")
        items = []
        next_link = hxs.select("//div[@class='pagination']/a[contains(text(), 'Siguiente')]/@href").extract()
        if next_link:
            yield Request("http://subdivx.com/" + next_link[0], callback=self.parse)

        for i in enumerate(titles):
            title = i[1].select("div/a/text()").extract()
            descr = contents[i[0]].select("div[@id='buscador_detalle_sub']/text()").extract()
            item = SubdivxItem()
            item["title"] = title[0] if title else None
            item["descr"] = descr[0] if descr else None
            yield Request(contents[i[0]].select("div[@id='buscador_detalle_sub_datos']/a[@target='new']/@href").extract()[0], callback=lambda x: self.parse_subtitle(x, item))
