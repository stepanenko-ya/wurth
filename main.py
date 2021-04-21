from bs4 import BeautifulSoup
import requests
import csv
# import psycopg2
# import re

# conn = psycopg2.connect(dbname='test', user='evgenijstepanenko',
#                         password='123456', host='localhost')
# db = conn.cursor()


proxies = {"http": "http://76.9.75.42:8080",
           "http": "http://88.198.24.108: 3128"}

GLOBAL_URL = 'https://wuerth.by/catalog_new/avtomobilnye_aksessuary/'
host = 'https://wuerth.by'


def get_html(url):
    qwe = requests.get(url, headers={'user-agent': 'Mozilla/5.0'}, proxies=proxies)
    return qwe


def take_item_urls():
    html = get_html(GLOBAL_URL)
    soup = BeautifulSoup(html.content, 'html.parser')
    url1 = soup.find_all(class_='menu_level_1 break-word list-reset')
    file = open('file2_csv.csv', 'w')

    for one in url1:
        first_level = one.find_all(class_='item_2')
        for two in first_level:
            two_level = two.find_all('a')
            for last in two_level:
                result_url1 = host + last.get('href')

                secondary_html = get_html(result_url1)
                secondary_soup = BeautifulSoup(secondary_html.content, "html.parser")
                res_secondary = secondary_soup.find_all(class_='media-body-old')
                for i in res_secondary:
                    url2 = host + i.find('a').get('href')
                    third_html = get_html(url2)
                    third_soup = BeautifulSoup(third_html.content, 'html.parser')
                    if third_soup.find(class_='wrap'):
                        four_urls = third_soup.find_all(class_='wrap')
                        for four_url in four_urls:
                            item_url = four_url.find(class_='title').find('a').get('href')
                            file.write(f'{host}{item_url}\n')
                print(result_url1)
    file.close()


def pars(lst_urls):
    x = 0
    csvfile = open('result.csv', 'w')
    fieldnames = ['Имя товара'+ '|'+  'Номер артикула' + '|'+'Ссылка карточки товара'+ '|'+ 'Описание'+ '|'+ 'Фото']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for url in lst_urls:
        item_html = get_html(url[0])
        four_soup = BeautifulSoup(item_html.content, 'html.parser')
        try:
            name = four_soup.find(class_='col-xs-12 col-sm-6 elem-descr-print').find(class_='catalog-title small').get_text().strip()
        except AttributeError:
            print("Error: ", url)
        else:
            vendor_code = four_soup.find(class_='col-xs-12 col-sm-6 elem-descr-print').find(class_='catalog-item--article-tovara').get_text().strip().split(":")[1]
            if four_soup.find(class_='col-xs-12 col-sm-6 elem-descr-print').find(class_='p'):
                description = four_soup.find(class_='col-xs-12 col-sm-6 elem-descr-print').find(class_='p').getText()
            else:
                description = ""

            photo = host + four_soup.find(class_='col-xs-12 col-sm-6 elem-slider-print').find('a').get('href')
            tree = four_soup.find(class_='breadcrumb').get_text().strip().replace('\n', "-")
            description = description.replace("\n", " ")
            desctipt = description.replace("\r", " ")

            if desctipt.count("'") % 2 != 0:
                desctipt = desctipt.replace("'", "''")


            x += 1
            print(x)
            # db.execute("INSERT INTO shop_by (item_name, description, photo) values ('"+ name+"', '"+desctipt+"', '"+photo+"')")
            # conn.commit()



        # csvfile.writelines('' + name + '|' + vendor_code + '|' + url[0]+ '|' + desctipt + '|' + photo + '\n')



def argyments(urls):
    file = open('params.csv', 'w')
    fieldnames = ['Артикул' + '|' + 'Параметр' + '|' + 'Значение параметра']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for url in urls:
        item_html = get_html(url[0])
        param_soup = BeautifulSoup(item_html.content, 'html.parser')

        vendor_code = param_soup.find(class_='col-xs-12 col-sm-6 elem-descr-print').find(class_='catalog-item--article-tovara').get_text().strip().split(":")[1]
        name = param_soup.find(class_='col-xs-12 col-sm-6 elem-descr-print').find(class_='catalog-title small').get_text().strip()
        parametrs = param_soup.find(class_='col-xs-12 col-md-6').find('tbody').find_all('tr')
        for parametr in parametrs:
            p = parametr.find_all("td")
            param_name = p[0].get_text().strip()
            param_value = p[1].get_text().strip()
            file.writelines(
                name + '|' + vendor_code + '|' + param_name + '|' + param_value + '\n')


if __name__ == '__main__':

    # lst_urls = take_item_urls()
    # db.execute("CREATE TABLE shop_by (id serial PRIMARY KEY,item_name text, description text, photo text)")
    # conn.commit()
    file_urls = open('file2_csv.csv', 'r')
    with open('/home/yevhen7/Documents/yana/porject/expiriment/file2_csv.csv','r') as file_urls:
        data = csv.reader(file_urls)
        # pars(data)
        argyments(data)
