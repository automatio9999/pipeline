from bs4 import BeautifulSoup
from random import uniform
from time import sleep
from req import new_session

def scrape_product_page(url: str) -> dict:
    session = new_session()
    res = session.get(url, impersonate="chrome")
    soup = BeautifulSoup(res.text, "html.parser")
    product_data = dict()
    title_elm = soup.find("h1", attrs={"data-testid": "product-title"})
    
    if title_elm:
        product_data.update(title=title_elm.get_text(strip=True))
        brand_elm = title_elm.find_previous_sibling()
        if brand_elm:
            product_data.update(brand=brand_elm.get_text(strip=True))

    id_elm = soup.find("span", class_="js-model")
    if id_elm:
        id = id_elm.get_text(strip=True)
        product_data.update(product_id=id)

    price_elm = soup.find("div", class_="js-product-prices")
    if price_elm:
        current_price = price_elm.get("data-price-amount")
        product_data.update(current_price=current_price)

    return product_data
