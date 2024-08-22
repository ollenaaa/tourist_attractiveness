from bs4 import BeautifulSoup
import json
import time
import random
import aiohttp
import asyncio
import re

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'}


async def scrape_google_serp_results(session, query: str) -> int:
    url = f"https://www.google.com/search?q={query}"

    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                print(f"Request to {url} was successful with status code 200")
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                result_stats = soup.find(attrs={"id": "result-stats"})
                if result_stats is None:
                    result_stats = await scrape_google_serp_results(session, query)
                    return result_stats
                
                result_stats = result_stats.text
                result_stats = result_stats.replace('\xa0', '')
                num_result = re.findall(r'\d+', result_stats)[0]
                return int(num_result)
            else:
                print(f"Error status: {response.status} for {url}")
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))


async def scrape_flightconnections_results(session, country: str, code: str) -> int:
    url = f"https://www.flightconnections.com/airports-in-{country}-{code}"

    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                print(f"Request to {url} was successful with status code 200")
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                result = soup.find('div', class_='site-title-text').find('p')

                if result is None:
                    print(f"No such element")
                    return 0

                countries_count = re.search(r'\b\d+\b(?=\s+countries)', result.text)
                return int(countries_count.group())
            else:
                print(f"Error status: {response.status} for {url}")
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))


async def scrape_booking_results(session, country: str) -> int:
    url = f"https://www.booking.com/searchresults.en-gb.html?ss={country}&ssne_untouched=Carpathians+-+Ukraine"

    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                print(f"Request to {url} was successful with status code 200")
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")
                result = soup.find(attrs={"class":"e037993315 f8da796a11"}).text
                result = result.replace(',', '')
    
                if not result:
                    return 0

                num_result = re.findall(r'\d{1,50}', result)[0]
                return int(num_result)
            else:
                print(f"Error status: {response.status} for {url}")
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))


async def scrape_civitatis_results(session, country: str) -> int:
    country = country.lower()
    url = f"https://www.civitatis.com/en/{country}/"

    try:
        # await asyncio.sleep(random.uniform(6, 9))
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                print(f"Request to {url} was successful with status code 200")
                html = await response.text()
                soup = BeautifulSoup(html, "lxml")

                num_attraction = soup.find_all(attrs={"class": "m-head-info__item__txt_big"})[1].text
                num_attraction = num_attraction.replace(",", "")

                num_impression = soup.find_all(attrs={"class": "m-head-info__item__txt_small"})[3].text
                num_impression = num_impression.replace(",", "")
                num_impression = re.findall(r'\d{1,50}', num_impression)[0]
                
                return int(num_attraction), int(num_impression)
            else:
                print(f"Error status: {response.status} for {url}")
                return None, None
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))    


# async def scrape_numbeo(session, country: str, query: str) -> float:
#     country = country.replace("-", "+")
#     url = f"https://www.numbeo.com/{query}/country_result.jsp?country={country}"

#     try:
#         async with session.get(url, headers=headers) as response:
#             if response.status == 200:
#                 html = await response.text()
#                 soup = BeautifulSoup(html, "html.parser")
#                 health_care = soup.find(attrs={"class": "table_indices"}).find(attrs={"style": "text-align: right"}).text
#                 return float(health_care)
#             else:
#                 print(f"Error status: {response.status} for {url}")
#     except aiohttp.ClientConnectorError as err:
#         print(f'Connection error: {url}', str(err))


async def scrape_country(session, country, code):
    requests = [
        scrape_flightconnections_results(session, country, code),
        scrape_google_serp_results(session, f'airport in {country}'),
        scrape_google_serp_results(session, f'taxi in {country}'),
        scrape_google_serp_results(session, f'public transport in {country}'),
        scrape_booking_results(session, country),
        scrape_google_serp_results(session, f'hotel in {country}'),
        scrape_google_serp_results(session, f'tourist attraction in {country}'),
        scrape_civitatis_results(session, country)
    ]

    num_air_links, num_airport, num_taxi, num_transport, num_hotel, hotel, num_attraction, attraction_impression = await asyncio.gather(*requests)

    return {
        'air links': num_air_links,
        'airport': num_airport,
        'taxi': num_taxi,
        'public transport': num_transport,
        'hotel': num_hotel,
        'search hotel': hotel,
        'impression': attraction_impression[1],
        'attraction': attraction_impression[0],
        'search attraction': num_attraction
    }


async def main():
    countries = {'Ukraine': 'ua', 'Poland': 'pl', 'France': 'fr', 'United-States': 'us', 'Spain': 'es', 'Bulgaria': 'bg'}
    data = {}

    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session1, \
            aiohttp.ClientSession(connector=conn) as session2, \
            aiohttp.ClientSession(connector=conn) as session3:
        
        tasks = []
        session_list = [session1, session2, session3]

        for i, (country, code) in enumerate(countries.items()):
            session = session_list[i % len(session_list)]
            task = asyncio.create_task(scrape_country(session, country, code))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        for country, result in zip(countries.keys(), results):
            data[country] = result

    json_data = json.dumps(data, indent=4)
    print(json_data)


if __name__ == "__main__":
    asyncio.run(main())