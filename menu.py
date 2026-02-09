import re

from bs4 import BeautifulSoup

def scrape_subcategories(soup: BeautifulSoup) -> list[dict]:
    subcategory_code = re.compile(r"(?<=/)\d+(?=-)")
    subcategory_list = []

    if soup is None:
        return subcategory_list

    sports_menu = soup.find(id="dmm-popover-1")
    if sports_menu is None:
        return subcategory_list

    category_selector = "div > div.main-nav_popover-content > nav > ul > li"
    subcategory_selector = "nav > ul > li > a"
    categories = sports_menu.select(category_selector)
    for category in categories:
        subcategories = category.select(subcategory_selector)
        exclude_last = len(subcategories) - 1
        for subcat in subcategories[:exclude_last]:
            url = subcat.get("href")
            if url is None or len(url) == 0:
                continue
            name = subcat.text.strip()
            found_code = subcategory_code.findall(url)
            code = 0
            if len(found_code) > 0:
                code = int(found_code[0])
            subcategory_list.append(dict(subcategory_name=name, subcategory_url=url, subcategory_code=code))
            break
        break
    #menu_selector = "#header > section > nav > ul > li"
    #menus = soup.select(menu_selector)
    #for menu in menus[:]:
    #    categories = menu.select(category_selector)
    #    for category in categories:
    #        subcategories = category.select(subcategory_selector)
    #        for subcategory in subcategories:
    #            sub.append(subcategory)

    return subcategory_list

