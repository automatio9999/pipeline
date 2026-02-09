import csv
from bs4 import BeautifulSoup
from req import new_session
from menu import scrape_subcategories
from subcategory import scrape_subcategory
from product import scrape_product_page
from random import uniform
from time import sleep
from json import dump

def delay(min: float, max:float):
    sleep(uniform(min, max))

def write_csv(filename, data):
    if not data:
        return
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["id","current_price","title", "brand","url","img_elm","category"])
        writer.writeheader()
        writer.writerows(data)

def cache_to_json_dict(filename: str, obj: list[dict]):
    with open(filename, "w", encoding="utf-8") as f:
        dump(obj, f, indent=4, sort_keys=False)


def crawl_categories(categories: list[dict]) -> list[dict]:
    crawl_data = []
    if len(categories) == 0:
        return crawl_data
    i = 0
    for subcategory in categories:
        print(subcategory)
        url = subcategory.get("subcategory_url")
        if url is None:
            continue
        if i > 0:
            delay(5,10)
        products = scrape_subcategory(url)
        print(products, len(products))
        for product in products:
            url = product.get("product_url")
            product.update(subcategory)
            if url:
                data = scrape_product_page(url)
                product.update(data)
                crawl_data.append(product) 
                delay(2,3)
            break
        i+=1

    return crawl_data

        
def main():
    #TODO:
    # hash products per page  with total products
    # categories = ["https://www.decathlon.ma/4838-shorts-bebe", "https://www.decathlon.ma/4841-chaussures-bebe"]
    session = new_session()
    res = session.get(f"https://www.decathlon.ma/", impersonate="chrome")
    soup = BeautifulSoup(res.text, "html.parser")
    subcategories = scrape_subcategories(soup)
    products = crawl_categories(subcategories)
    cache_to_json_dict("data.json", products) 
    #products_sorted_by_id = sorted(products, key=lambda item: item['id'])
    #write_csv("data.csv", products_sorted_by_id) 


if __name__ == "__main__":
    main()
