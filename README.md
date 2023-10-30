# Scrapy Parser Maksavit

## Парсинг сайта аптеки Maksavit
Асинхронный парсер собирающий данные о товарах с сайта `https://maksavit.ru`.
С каждой страницы товара парсер собирает название, цену, характеристики товара и сохраняет файл с расширением .json.

## Технологии проекта
* Python — высокоуровневый язык программирования.
* Scrapy — популярный фреймворк для парсинга веб сайтов.

## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Semavova/scrapy_parser_maksavit.git
```

Создать и активировать виртуальное окружение:
```
python -m venv env
```

```
source venv/Scripts/activate
```

Обновить менеджер пакетов pip и установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

## Запуск парсера
```
scrapy crawl maksavit -a start_urls="URL, URL" -a products_count=int
```
Где URL - страницы категории товаров, разделенных запятыми. products_count - количество товаров для парсинга

Автор: [Владимир Семочкин](https://github.com/Semavova)