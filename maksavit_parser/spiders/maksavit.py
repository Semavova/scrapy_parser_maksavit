import datetime as dt

import scrapy

from maksavit_parser.items import MaksavitParserItem

LIMIT_EXCEEDED_MSG = "Достигнут лимит элементов"


class MaksavitSpider(scrapy.Spider):
    name = "maksavit"
    allowed_domains = ["maksavit.ru"]
    parsed_products_count = 0
    start_urls = []
    cookies = {
        'location_code': '0000949228',
        'location_selected': 'Y'
    }
    product_link_selector = 'a.product-card-block__title'
    next_page_selector = (
        'li:has(a.ui-pagination__item_checked) + li a::attr(href)'
    )
    current_price_selector = 'span.price-value::text'
    original_price_selector = 'div.price-box__old-price::text'
    brand_selector = 'a.product-info__brand-value::text'
    tags_selector = 'div.badges.product-picture__badges-position div::text'
    description_selector = (
        'div.ph23::text, div.ph23 p::text, div.ph23 span::text'
    )
    section_selector = 'li.breadcrumbs__item span::text'
    option_selector = 'div.product-info div[class$="subtitle"]::text'
    option_value_selector = (
        'div.product-info div[class$="subtitle"] + a::text,'
        'div.product-info div[class$="subtitle"] + div a::text'
    )
    stock_selector = 'div.available-count'
    variants_selector = 'div.quantity-items-wrapper div'
    title_selector = 'h1.product-top__title::text'
    main_image_selector = 'img.preload-image.product-image::attr(src)'

    def __init__(self, products_count=100, *args, **kwargs):
        super(MaksavitSpider, self).__init__(*args, **kwargs)
        self.products_count = int(products_count)
        self.start_urls = kwargs.get('start_urls').split(',')

    def parse(self, response):
        for product_link in response.css(self.product_link_selector):
            yield response.follow(
                product_link,
                callback=self.parse_product,
                cookies=self.cookies
            )
        next_page = response.css(self.next_page_selector).get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        self.parsed_products_count += 1
        if self.parsed_products_count >= self.products_count:
            self.crawler.engine.close_spider(self, LIMIT_EXCEEDED_MSG)
        current = response.css(self.current_price_selector).get()
        current = float(
            current.strip(' ₽').replace(" ", "")
        ) if current else None
        original = response.css(self.original_price_selector).get()
        original = float(
            original.strip(' \n ₽').strip().replace(" ", "")
        ) if original else current
        discount = 100-(100*current/original) if original != current else None
        brand = response.css(self.brand_selector).get()
        tags = response.css(self.tags_selector).getall()
        description = response.css(self.description_selector).getall()
        section = response.css(self.section_selector).getall()
        option = response.css(self.option_selector).getall()
        option_value = response.css(self.option_value_selector).getall()
        options_dict = {
            option: value.strip('\n ') if value
            else None for option, value in zip(option, option_value)
        }
        stock = response.css(self.stock_selector).get()
        metadata = {"__description": description}
        variants = len(response.css(self.variants_selector).getall())
        yield MaksavitParserItem({
            "timestamp": dt.datetime.now(),
            "RPC": response.request.url.split('/')[-2],
            "url": response.request.url,
            "title": response.css(self.title_selector).get(),
            "marketing_tags": [tag.strip('\n ') for tag in tags],
            "brand": brand.strip('\n ').split(',')[0] if brand else None,
            "section": section[:-1],
            "price_data": {
                "current": current,
                "original": original,
                "sale_tag": f"Скидка {discount:.2f}%" if discount else None
            },
            "stock": {
                "in_stock": True if stock else False,
            },
            "assets": {
                "main_image": self.allowed_domains[0] + response.css(
                    self.main_image_selector
                ).get(),
            },
            "metadata": {**metadata, **options_dict},
            "variants": variants
        })
