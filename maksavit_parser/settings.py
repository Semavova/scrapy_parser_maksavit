BOT_NAME = "maksavit_parser"

SPIDER_MODULES = ["maksavit_parser.spiders"]
NEWSPIDER_MODULE = "maksavit_parser.spiders"
ROBOTSTXT_OBEY = True
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
COOKIES_DEBUG = True
FEEDS = {
    'maksavit_%(time)s.json': {
        'format': 'json',
        'fields': [
            'timestamp',
            'RPC',
            'url',
            'title',
            'marketing_tags',
            'brand',
            'section',
            'price_data',
            'stock',
            'assets',
            'metadata',
            'variants',
        ],
        'overwrite': True
    }
}
