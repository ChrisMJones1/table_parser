import scrapy
from unicodedata import normalize


class TableSpider(scrapy.Spider):
    name = "tables"

    def start_requests(self):
        allowed_domains = ["https://web.tmxmoney.com"]
        urls = [
            "https://web.tmxmoney.com/article.php?newsid=8228797764093477&qm_symbol=ATD.B",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        table_list = []
        for table in response.xpath("./descendant::table[4]"):
            for row in table.xpath("./descendant::tr"):
                row_list = []
                for text in row.xpath("./descendant::td"):
                    text_return = text.xpath("./descendant::text()").extract()
                    text_return = "".join(text_return)
                    text_return = normalize('NFKD', text_return)
                    text_return = text_return.rstrip('\n')
                    row_list.append(text_return)

                table_list.append(row_list)

        yield {"table": table_list}
