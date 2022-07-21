from numpy import append
import requests
from bs4 import BeautifulSoup
import pandas as pd

pg_numbers = []
each_page_title = []
product_list = []
global count_url

# collecting soup and extract according to the URL

def extract(soup):
    # divs = soup.find_all('div',class_ = "p-item-img")
    divs = soup.find_all('div', class_ = "p-item")

    for links in divs:

        collect_links = links.a['href']
        # print(collect_links)

        details_url = collect_links
        details_r = requests.get(details_url)
        details_soup = BeautifulSoup(details_r.content, 'lxml')
        title = details_soup.find('h1', class_ = "product-name").text
        # print(title)

                
        try:
            price = details_soup.find('td', class_ = "product-info-data product-price").text.replace('৳', '')
        except:
            price = ""
        # print(price)

        try:
            regular_price = details_soup.find('td', class_ = "product-info-data product-regular-price").text.replace('৳', '')
        except:
            regular_price = ""
        # print(regular_price)

        try:
            status = details_soup.find('td', class_ = "product-info-data product-status").text
        except:
            status = ""
        # print(status)

        try:
            product_code = details_soup.find('td', class_ = "product-info-data product-code").text
        except:
            product_code = ""
        # print(product_code)

        try:
            product_brand = details_soup.find('td', class_ = "product-info-data product-brand").text
        except:
            product_brand = ""
        # print(product_brand)

        try:
            key_feature = details_soup.find('div', class_ = "short-description").ul.text.replace('View More Info','')
        except:
            key_feature = ""    

        # print(key_feature)


        # key_feature = details_soup.find('div', class_ = "short-description").ul.text.replace('View More Info','')
        # print(key_feature)
        # print("\n")

        try:
            description = details_soup.find('div', class_ = "full-description").text
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




def url(page,count_url):
    url_list = [
        f"https://www.startech.com.bd/desktops?page={page}",
        f"https://www.startech.com.bd/component/ram?page={page}",
        f"https://www.startech.com.bd/component/graphics-card?page={page}",
        f"https://www.startech.com.bd/laptop-notebook?page={page}",
        f"https://www.startech.com.bd/laptop-notebook/laptop-accessories?page={page}",
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
            r = requests.get(i)
            soup = BeautifulSoup(r.content, 'lxml')
            page_number = soup.find('div', class_ = "col-md-6 rs-none text-right").p.text.split("(")[-1].replace(' Pages)','')
            page_title = soup.find('h6', class_ = "page-heading m-hide").text
            # print(page_number)
            pg_numbers.append(int(page_number))
            each_page_title.append(page_title)
        
    else:
        new_url = url_list[count_url]
        print(new_url)
        r = requests.get(new_url)
        soup = BeautifulSoup(r.content, 'lxml')
        return soup



def main():
    
    # fls = -1
    count_url = -1
    url(1,count_url)
    print(pg_numbers)

    # print(len(pg_numbers))
    # for page_number in pg_numbers:
    #     print(type(page_number))
    count_url = 0
    page_number_of_title = 0
    # fls = 1

    for page_number in pg_numbers:
        # print(f"page title {each_page_title[page_number_of_title]}")
        title = each_page_title[page_number_of_title]
        page_number_of_title = page_number_of_title + 1
        for j in range(1,page_number+1):
            print(f"Scraping page {j}.....!")
            soup_from_given_url = url(j,count_url)
            extract(soup_from_given_url)
        count_url = count_url + 1
        df = pd.DataFrame(product_list)
        df.to_csv(f"{title}"".csv")
        product_list.clear()


if __name__ == "__main__":
    main()
