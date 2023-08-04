# Django imports
from django.shortcuts import get_object_or_404

# Third-party imports
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import asyncio
from bs4 import BeautifulSoup
from products.utils import (
    lookup_prices,
    extract_name,
    extract_rating_and_comments,
)
import math

from celery import shared_task
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# Local imports
from .models import Product
from .serializers import ProductsSerializer
from bot import finished_parsing

from asgiref.sync import async_to_sync

class ProductsListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        products_count = request.data.get('products_count', 10)
        if products_count > 50 or products_count <= 0:
            parsed_products = parse_ozon_products(50)
        else:
            parsed_products = parse_ozon_products(products_count)
        serializer = ProductsSerializer(data=parsed_products, many=True)
        if serializer.is_valid():
            serializer.save()
            finished = async_to_sync(finished_parsing)
            finished(products_count)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductsSerializer(product)
        return Response(serializer.data)



def soup_func(filename: str):
    with open(filename, "r+") as index:
        soup = BeautifulSoup(index, "html.parser")
        return soup
    
def generate_link(product_count: int = 10) -> int:
    calculated_page = math.ceil(product_count / 36)
    return f"https://www.ozon.ru/seller/proffi-1/products/?miniapp=seller_1&page={calculated_page}"

@shared_task
def parse_ozon_products(products_count=10):
    
    ua = UserAgent()
    user_agent = ua.random
    chrome_options = Options()
    chrome_options.add_argument("--headless")    
    chrome_options.add_argument(f"user-agent={user_agent}")
        
    driver = webdriver.Chrome(options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
        'source':'''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })
    
    url = generate_link(products_count)
    
    driver.get(url)
    
    all_cookies = driver.get_cookies()
    for cookie in all_cookies:
        driver.add_cookie(cookie)
        
        
    if "Your browser is out of date" in driver.page_source:
        print("Error: Your browser is out of date. Please update your browser or use a different one.")
        driver.refresh()
        time.sleep(5)
        
    
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    products = (
        soup.find("div", attrs={"id": "paginatorContent"})
        .find("div")
        .find("div")
        .find_all("div", recursive=False)
    )

    result = []
        
    for product in products[:products_count]:
        link = product.find("a")["href"]
        [price, old_price, discount] = lookup_prices(product)
        name = extract_name(product)
        [rating, feedback] = extract_rating_and_comments(product)
        result.append(
            {
                "link": link,
                "new_price": float(price),
                "old_price": float(old_price),
                "discount": discount,
                "name": name,
                "rating": float(rating),
                "feedback": int(feedback),
            }
        )
        
        time.sleep(1)
    
    driver.quit()
    return result
