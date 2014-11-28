from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from MEMSbooks.items import booksItem


class booksSpider(CrawlSpider):
    download_delay = 5  # The server will force to disconnect your download if no delay 
    name = "books"
    allowed_domains = ["crcnetbase.com"]
    start_urls = ["http://www.crcnetbase.com/action/doSearch?AllField=MEMS&access=user&pageSize=20&content=title&target=titleSearch"]

    rules = (   Rule(SgmlLinkExtractor(allow = (), restrict_xpaths = ("//a[contains(@href, '/isbn/')]")), callback = "", follow=True), 
                Rule(SgmlLinkExtractor(allow = (), restrict_xpaths = ("//a[@target='_blank' and @class='articleListing_links' and contains(text(), 'Hi')]")), callback="parse_chapter"),
            )            
            
    def parse_start_url(self, response):
        sel = Selector(response)
        books = sel.xpath("//ul[@class='bookTitleList']//li//a/text()").extract()
        print "%d books detected:===========================".format(len(books))
        print "\n".join(books)
        
    def parse_chapter(self, response):
        print ":::::::::::::::::::::::::::::::::::::::::::::"
        fname = response.url.split("/")[-1].replace(".", "_")  
        fname = fname+".pdf"
        with open(fname, "wb") as f:
            f.write(response.body)
        print "Downloaded: ", fname