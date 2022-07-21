#It's not working

from aiohttp import ClientSession
import asyncio
import pathlib
from numpy import append
# import requests
from bs4 import BeautifulSoup
import pandas as pd

# async def main():
#     url = ""
#     async with ClientSession() as session:
#         async with session.get(url) as response:


pg_numbers = []
product_list = []
global count_url


# def passing_soup(url):
#     # url = f"https://www.startech.com.bd/laptop-notebook/laptop?page={page}"
    
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'lxml')
#     # print(url)
#     return soup



# def page(soup):
#     # divs = soup.find_all('div', class_ = "p-item")
#     try:
#         page = soup.find('div', class_ = "col-md-6 rs-none text-right").p.text.split("(")[-1].replace(' Pages)','')
#     except:
#         page = ""
#     return page


async def extract(soup):
    # divs = soup.find_all('div',class_ = "p-item-img")
    divs = await soup.find_all('div', class_ = "p-item")

    for links in divs:

        collect_links = links.a['href']
        # print(collect_links)
        async with ClientSession() as request:
            details_url = await collect_links
            details_r = await request.get(details_url)
            details_soup = await BeautifulSoup(details_r.content, 'lxml')
            title = await details_soup.find('h1', class_ = "product-name").text
            # print(title)

                
        try:
            price = await details_soup.find('td', class_ = "product-info-data product-price").text.replace('৳', '')
        except:
            price = ""
        # print(price)

        try:
            regular_price = await details_soup.find('td', class_ = "product-info-data product-regular-price").text.replace('৳', '')
        except:
            regular_price = ""
        # print(regular_price)

        try:
            status = await details_soup.find('td', class_ = "product-info-data product-status").text
        except:
            status = ""
        # print(status)

        try:
            product_code = await details_soup.find('td', class_ = "product-info-data product-code").text
        except:
            product_code = ""
        # print(product_code)

        try:
            product_brand = await details_soup.find('td', class_ = "product-info-data product-brand").text
        except:
            product_brand = ""
        # print(product_brand)

        try:
            key_feature = await details_soup.find('div', class_ = "short-description").ul.text.replace('View More Info','')
        except:
            key_feature = ""    

        # print(key_feature)


        # key_feature = details_soup.find('div', class_ = "short-description").ul.text.replace('View More Info','')
        # print(key_feature)
        # print("\n")

        try:
            description = await details_soup.find('div', class_ = "full-description").text
        except:
            description = ""
        # print(description)

        

        product = {
            'Product Name' : title,
            'Product Price': price,
            'Regular Price': regular_price,
            'Product Status': status,
            'Product Code' : product_code,
            'Brand' : product_brand,
            'Key Feature' : key_feature,
            'Description' : description,
        }
        product_list.append(product)

    return




async def url(page,count_url):
    url_list = [
    f"https://www.startech.com.bd/desktops?page={page}",
    f"https://www.startech.com.bd/laptop-notebook?page={page}",
    f"https://www.startech.com.bd/laptop-notebook/laptop-accessories?page={page}",
    f"https://www.startech.com.bd/component/graphics-card?page={page}",
    f"https://www.startech.com.bd/component/ram?page={page}",
    f"https://www.startech.com.bd/component/SSD-Hard-Disk?page={page}",
    f"https://www.startech.com.bd/component/casing?page={page}",
    f"https://www.startech.com.bd/monitor?page={page}",
    f"https://www.startech.com.bd/ups-ips?page={page}",
    f"https://www.startech.com.bd/office-equipment/printer?page={page}",
    f"https://www.startech.com.bd/office-equipment/toner?page={page}",
    f"https://www.startech.com.bd/office-equipment?page={page}",
    f"https://www.startech.com.bd/camera?page={page}",
    f"https://www.startech.com.bd/Security-Camera?page={page}",
    f"https://www.startech.com.bd/networking/router?page={page}",
    f"https://www.startech.com.bd/networking/network-switch?page={page}",
    f"https://www.startech.com.bd/accessories/keyboards?page={page}",
    f"https://www.startech.com.bd/accessories/mouse?page={page}",
    f"https://www.startech.com.bd/accessories/headphone?page={page}",
    f"https://www.startech.com.bd/accessories/speaker-and-home-theater?page={page}",
    f"https://www.startech.com.bd/accessories/bluetooth-speaker?page={page}",

    ]
    # print(len(url))
    flss = count_url
    if flss == -1:
        for i in url_list:
            async with ClientSession() as request:
                # async with session.get(url) as response:
                r = await request.get(i)
                soup = await BeautifulSoup(r.content, 'lxml')
                page_number = soup.find('div', class_ = "col-md-6 rs-none text-right").p.text.split("(")[-1].replace(' Pages)','')
                # print(page_number)
                pg_numbers.append(int(page_number))
        
    else:
        new_url = url_list[count_url]
        print(new_url)
        async with ClientSession() as request:
            r = await request.get(new_url)
            soup = await BeautifulSoup(r.content, 'lxml')
            return soup



async def main():

    async with ClientSession() as session:
        async with session.get(url) as response:
            html_body = await response.read()
    count_url = -1
    await url(1,count_url)
    print(pg_numbers)

    # print(len(pg_numbers))
    # for page_number in pg_numbers:
    #     print(type(page_number))
    count_url = 0
    # fls = 1
    for page_number in pg_numbers:
        for j in range(1,page_number):
            print(f"Scraping page {j}.....!")
            soup_from_given_url = await url(j,count_url)
            await extract(soup_from_given_url)
        count_url = count_url + 1


results = asyncio.run(main())


# if __name__ == "__main__":
#     main()
