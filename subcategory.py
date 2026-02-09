from bs4 import BeautifulSoup
from random import uniform
from time import sleep
from req import new_session


def delay(min: float, max:float):
    sleep(uniform(min, max))


def scrape_subcategory(category_url: str, page: int = 1) -> list[dict]:
    delay(2, 3)
    session = new_session()
    res = session.get(f"{category_url}?page={page}", impersonate="chrome")
    #print(f"{category_url}?page={page}")
    soup = BeautifulSoup(res.text, "html.parser")
    div = soup.find("div", attrs={"data-testid": "products-list"})
    items = []
    if div:
        for product in div.select(".js-product-list > li"):
            a = product.find("a")
            item = dict()
            if a:
                img_elm = a.find("img")
                url = a.get("href")
                item.update(dict(product_url=url))
                if img_elm:
                    img = img_elm.get("src")
                    item.update(dict(product_img=img))

                sku_elm = product.find("article")
                if sku_elm:
                    sku = sku_elm.get("data-sku")
                    item.update(dict(product_sku=sku))
                items.append(item)
    # Recursive category pagination
    pagination = soup.find("div", attrs={"data-testid": "pagination-list"})
    if pagination:
        page_count = pagination.get("data-page-count")
        if page_count:
            page_count = int(page_count)
            if page < page_count:
                items.extend(scrape_subcategory(category_url, page + 1))
    return items
