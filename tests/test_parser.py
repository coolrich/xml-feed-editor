import gc
import pprint
import sys

from bs4 import BeautifulSoup
from lxml import etree
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def myparser(file_path):
    parser = etree.XMLParser(huge_tree=True, encoding="windows-1251")
    tree = etree.parse(file_path, parser=parser)
    category_elems = tree.xpath("//category")
    category_ids_names = {}

    categories = set()
    for category in category_elems:
        category_id = category.get("id").strip()
        category_name = category.text.strip()
        categories.add(category_name)
        category_ids_names[category_id] = category_name

    category_products_dict = {}
    for category in categories:
        category_products_dict[category] = []

    offer_tags = tree.xpath("//offer")
    for offer_tag in offer_tags:
        category_id = offer_tag.xpath("categoryId")
        product_name = offer_tag.xpath("name")
        cid = category_id[0].text.strip()
        print(cid)
        if cid not in category_ids_names:
            continue
        category_name = category_ids_names[cid]
        category_products_dict[category_name].append(product_name[0].text)
    pprint.pp(category_products_dict)

    del tree, categories, offer_tags
    gc.collect()
    return category_products_dict


path = "products_catalog.xml"
print(myparser(path))
