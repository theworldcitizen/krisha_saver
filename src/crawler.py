from bs4 import BeautifulSoup
import requests
from models import Ad, Location, Author, Result, Details
from itertools import chain
import itertools

ENTRY_POINT = 'https://krisha.kz/'


class Crawler:
    headers = {
        'authority': 'krisha.kz',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://krisha.kz/',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    # def __init__(self, channel):
    #     self.channel = channel

    def make_request(self, url: str):
        html = requests.get(ENTRY_POINT + url, headers=self.headers)
        print(html.status_code)
        print(ENTRY_POINT+url)
        if html.ok:
            return html.text

    def get_soup(self, html) -> BeautifulSoup:
        soup = BeautifulSoup(html, "html.parser")
        return soup

    @staticmethod
    def get_title(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_='layout__content')
            div = content.find('div', class_='offer__advert-title')
            title = div.find('h1').text.strip()
            return title
        except Exception:
            return None

    @staticmethod
    def get_ad_number(soup: BeautifulSoup):
        content = soup.find('div', class_='layout__container main-col a-item')
        ad_number = content.get('data-id')
        return ad_number

    @staticmethod
    def get_category(soup: BeautifulSoup):
        full_content = soup.find('main', class_='container')
        content = full_content.find('section', class_='breadcrumbs breadcrumbs-top ')
        divs = content.find_all('div')
        res = divs[1].text
        return res

    @staticmethod
    def get_description(soup: BeautifulSoup):
        try:
            container = []
            output = ''
            content = soup.find('div', class_='offer__description')
            divs = content.find_all('div')
            for div in divs:
                info = div.text.strip()
                container.append(info)
                result = output.join(container)
                result = result.strip()
            return result
        except Exception:
            return None

    @staticmethod
    def get_price(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_='offer__advert-info')
            divs = content.find_all('div')
            price = divs[0].text.strip()
            return price
        except Exception:
            return None

    @staticmethod
    def get_photo(soup: BeautifulSoup):
        try:
            photos = []
            content = soup.find('div', class_='gallery__container')
            table = content.find('ul', class_='gallery__small-list')
            li_elemets = table.find_all('li')
            for li in li_elemets:
                data = li.find('picture')
                image = data.find('img')
                url_of_photo = image.get('src')
                photos.append(url_of_photo)
            return photos
        except Exception:
            return None

    @staticmethod
    def get_publish_date(soup: BeautifulSoup):
        content = soup.find('div', class_='main-col a-item')
        data = content.find('div', class_='offer__views')
        divs = data.find_all('div')
        res = divs[1].text.strip()
        li = list(res.split(" "))
        day = li[-2]
        month = li[-1]
        publish_date = day + ' ' + month
        return publish_date

    @staticmethod
    def get_city(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_='offer__short-description')
            divs = content.find_all('div')
            div = divs[3].text.strip()
            li = list(div.split(" "))
            city = li[0]
            city = city.replace(',', '')
            return city
        except Exception:
            return None

    @staticmethod
    def get_region(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_='offer__short-description')
            divs = content.find_all('div')
            div = divs[3].text.strip()
            li = list(div.split(" "))
            region_name = li[1]
            region_type = li[2]
            region_type = region_type.replace('\nпоказать', '')
            full_region = region_name + ' ' + region_type
            return full_region
        except Exception:
            return None

    @staticmethod
    def get_address(soup: BeautifulSoup):
        address = ''
        content = soup.find('div', class_='layout__content')
        div = content.find('div', class_='offer__advert-title')
        title = div.find('h1').text.strip()
        li = list(title.split(" "))
        response = li[6:]
        for word in response:
            address = address + ' ' + word
        address = address.strip()
        return address

    @staticmethod
    def get_id_of_author(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_='offer__sidebar-item offer__sidebar-contacts')
            divs = content.find_all('div')
            div = divs[2]
            id_of_author = div.get('data-id')
            return id_of_author
        except Exception:
            return None

    @staticmethod
    def get_name_of_author(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_='offer__sidebar-item offer__sidebar-contacts')
            divs = content.find_all('div')
            div = divs[2]
            res = div.find('a', class_='owners__name')
            name = res.text
            return name
        except Exception:
            return None

    @staticmethod
    def get_phone_number(soup: BeautifulSoup):
        try:
            numbers = []
            content = soup.find('div', class_='offer__sidebar-item offer__sidebar-contacts')
            div = content.find('div', class_='offer__contacts')
            div1 = div.find('div', class_='a-phones')
            n = div1.find('div', class_='offer__contacts-loaded')
            n2 = n.find('div', class_='offer__contacts-phones')
            p_tags = n2.find_all('p')
            for p in p_tags:
                number = p.text
                # print(number)
            br = div1.find('div', class_='skeleton-block')
            div2 = br.find('div', class_='a-phones__hidden')
            result = div2.find('span', class_='phone')
            # print(result.text)
            return numbers
        except Exception:
            return None

    @staticmethod
    def get_author_type(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_='offer__sidebar-item offer__sidebar-contacts')
            divs = content.find_all('div')
            type_of_author = divs[5].text
            return type_of_author
        except Exception:
            return None

    @staticmethod
    def get_author_url(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_='offer__sidebar-item offer__sidebar-contacts')
            divs = content.find_all('div')
            div = divs[2]
            res = div.find('a', class_='owners__name')
            url = res.get('href')
            return ENTRY_POINT + url
        except Exception:
            return None

    @staticmethod
    def get_rating(soup: BeautifulSoup):
        content = soup.find('div', class_='offer__content')
        div = content.find('div', class_='left')
        divs = div.find_all('div')
        a = content.text
        print(a)
        div = content.find_all('div')
        print(div)
        div1 = div.find('div', class_='a-analytics-container')
        div2 = div1.find('div', class_='left')
        divs = div2.find_all('div')
        rating = divs[3].text
        return rating

    @staticmethod
    def get_payment_method(soup: BeautifulSoup):
        payment_methods = []
        try:
            content = soup.find('div', class_='offer__advert-info')
            div = content.find('div', class_='offer__sidebar-header')
            spans = div.find_all('span')
            for span in spans:
                method = span.text.strip()
                payment_methods.append(method)
            return payment_methods
        except Exception:
            return None

    @staticmethod
    def get_timetable(soup: BeautifulSoup):
        try:
            content = soup.find('div', class_='offer__sidebar-item offer__sidebar-contacts')
            divs = content.find_all('div')
            div = divs[2]
            res = div.find('a', class_='owners__name')
            url = res.get('href')
            html = requests.get(ENTRY_POINT + url)
            html = html.text
            bsoup = BeautifulSoup(html, 'html.parser')
            page = bsoup.find('div', class_='company-info__schedule')
            schedule = page.find('div', class_='company-info__time').text
            return schedule
        except Exception:
            return None

    def parse_link(self, link: str):
        result = []

        html = self.make_request(link)
        soup = self.get_soup(html)
        title = self.get_title(soup)
        ad_number = self.get_ad_number(soup)
        # category = self.get_category(soup)
        description = self.get_description(soup)
        price = self.get_price(soup)
        photo = self.get_photo(soup)
        publish_date = self.get_publish_date(soup)
        apartment_details = Ad(title=title, ad_number=ad_number,
                               ad_text=description, sum=price, photo=photo, url=ENTRY_POINT + link,
                               publish_date=publish_date)

        city = self.get_city(soup)
        region = self.get_region(soup)
        address = self.get_address(soup)
        location_info = Location(city=city, region=region, address=address)

        authors_id = self.get_id_of_author(soup)
        name_of_author = self.get_name_of_author(soup)
        phone_numbers = self.get_phone_number(soup)  # todo: check
        author_type = self.get_author_type(soup)
        author_url = self.get_author_url(soup)
        # email_of_author -> impossible to get
        author_info = Author(id=authors_id, name=name_of_author, phone=phone_numbers, author_type=author_type,
                             url=author_url)

        # rating = self.get_rating(soup) #todo: impossible to reach div's content
        payment_method = self.get_payment_method(soup)
        timetable = self.get_timetable(soup)
        details = Details(payment_method=payment_method, timetable=timetable)
        output = Result(ad=apartment_details, address=location_info, author=author_info, details=details).dict()


        return output

    def get_ad(self, link):
        result = []

        res = self.parse_link(link)

        return res


if __name__ == "__main__":
    result = Crawler().get_ad('https://krisha.kz/a/show/673151811')
    from pprint import pprint

    pprint(result)
