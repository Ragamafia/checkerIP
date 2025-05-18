import aiohttp
import asyncio
import json

from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

from sources import IPInfo, IPAPI, DBIP, IP2Location, ScamAlytics
#from logger import logger
from config import cfg


class IPChecker():
    ip: str
    checkers: list[callable]
    session: aiohttp.ClientSession

    def __init__(self, ip):
        self.ip = ip
        self.checkers = [
            self.scamalytics,
            self.ipinfo,
            self.ipapi,
            self.db_ip,
            self.ip2location,
        ]

        self.headers = {
            "User-Agent": UserAgent().random,
            "Accept": "*/*",
            "Accept-Language": "en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

    async def check(self):
        async with aiohttp.ClientSession() as self.session:
            tasks = [checker() for checker in self.checkers]
            results = await asyncio.gather(*tasks)
            print({k: v for r in results if r for k, v in r.items()})
            return {k: v for r in results if r for k, v in r.items()}

    async def request(self, url,
                      method=None,
                      use_proxy=False,
                      get_json=True,
                      attempts=5):
        if not self.session:
            print('No session')
            #logger.error("No session")
            return

        kwargs = {
            "url": url,
            "method": method or "GET",
            "headers": self.headers,
        }
        if use_proxy:
            kwargs["proxy"] = cfg.proxy

        try:
            async with self.session.request(**kwargs) as response:
                if response.status < 300:
                    if get_json:
                        try:
                            return await response.json()
                        except Exception:
                            print(f"{url}: Error get JSON - fall back to text.")
                    return await response.text()
                elif response.status >= 500:
                    raise ConnectionError(f'Server error {response.status}')
        except Exception as e:
            print(f'Error requesting attempt {attempts} {url}: {e}')
            #logger.warning(f'Error requesting attempt {attempts} {url}: {e}')
            attempts -= 1
            if attempts > 0:
                return await self.request(
                    url,
                    method=method,
                    use_proxy=use_proxy,
                    get_json=get_json,
                    attempts=attempts,
                )

    async def scamalytics(self):
        url = f"http://scamalytics.com/ip/{self.ip}"
        if data := await self.request(url, get_json=False, use_proxy=True):
            soup = bs(data, "html.parser")
            maps = {
                "Country Name": "country",
                "State / Province": "state",
                "District / County": "city",
                "City": "city",
                "Postal Code": "zip",
                "Latitude": "latitude",
                "Longitude": "longitude",
                "Datacenter": "is_datacenter",
                "Anonymizing VPN": "is_vpn",
                "Tor Exit Node": "is_tor",
                "Server": "is_crawler",
                "Public Proxy": "is_proxy_public",
                "Web Proxy": "is_proxy_web",
                "Search Engine Robot": "is_scanner",
            }
            values = {"Yes": True, "No": False, "Unknown": None}
            temp = {}
            for tr in soup.find('table').find_all('tr'):
                if (th := tr.find('th')) and (td := tr.find('td')):
                    if key := maps.get(th.text):
                        temp[key] = values.get(td.text, td.text)

            result = {k: v for k, v in temp.items() if "is_proxy" not in k}
            result["is_proxy"] = temp["is_proxy_public"] or temp["is_proxy_web"]
            if score := soup.find('div', {'class': 'score'}):
                result["fraud_score"] = int(score.text.split(': ')[-1].strip())
            return {"scamalytics": ScamAlytics(**result)}
        return {}

    async def ipinfo(self):
        url = f"http://ipinfo.io/{self.ip}"
        if data := await self.request(url, get_json=False):
            soup = bs(data, "html.parser")
            for script in soup.find_all('script'):
                if '"@type": "place"' in script.text:
                    if data := json.loads(script.text):
                        return {'ipinfo': IPInfo.from_response(data)}

    async def ipapi(self):
        url = f"http://api.ipapi.is/?q={self.ip}"
        if data := await self.request(url):
            return {'ipapi': IPAPI.from_response(data)}

    async def db_ip(self):
        url = f'http://db-ip.com/demo/home.php?s={self.ip}'
        if data := await self.request(url, use_proxy=True):
            if error := data.get("demoInfo", {}).get("error"):
                print(f"Error: {error}")
            else:
                return {'db-ip': DBIP.from_response(data)}
            return {}

    async def ip2location(self):
        url = f'http://www.ip2location.io/{self.ip}'
        if data := await self.request(url, get_json=False):
            soup = bs(data, "html.parser")
            for tag in soup.find_all('pre'):
                data = json.loads(tag.text)
                return {'ip2location': IP2Location.from_response(data)}
            return {}
