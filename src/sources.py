from pydantic import BaseModel


class BaseSource(BaseModel):
    name: str

    country: str
    state: str
    city: str
    zip: str | int | None

    latitude: float = None
    longitude: float = None
    map_url: str | None = None

    fraud_score: int | str | None = None
    isp: str | None = None

    has_type: bool | None = True
    is_bogon: bool | None = None
    is_mobile: bool | None = None
    is_satellite: bool | None = None
    is_crawler: bool | None = None
    is_datacenter: bool | None = None
    is_tor: bool | None = None
    is_proxy: bool | None = None
    is_vpn: bool | None = None
    is_abuser: bool | None = None
    is_spammer: bool | None = None
    is_scanner: bool | None = None
    is_botnet: bool | None = None

    def __str__(self):
        return (
            f"\n{self.name}\n"
            f"Country:   {self.country}\n"
            f"State:     {self.state}\n"
            f"City:      {self.city}\n"
            f"Zip:       {self.zip}\n"
            f"Latitude:  {self.latitude}\n"
            f"Longitude: {self.longitude}\n"
        )


class ScamAlytics(BaseSource):
    name: str = "ScamAlytics"


class IPInfo(BaseSource):
    has_type: bool = False

    @classmethod
    def from_response(cls, response: dict):
        address = response.get("contentLocation", {}).get("address", {})
        geo = response.get("contentLocation", {}).get("geo", {})
        return cls(
            name="IpInfo",
            country=address.get("addressCountry"),
            state=address.get("addressRegion"),
            city=address.get("streetAddress"),
            zip=address.get("PostalCode"),
            latitude=geo.get("latitude", 0.0),
            longitude=geo.get("longitude", 0.0),
            map_url=response.get("contentLocation", {}).get("hasMap"),
        )


class IPAPI(BaseSource):
    @classmethod
    def from_response(cls, response: dict):
        company = response.get("company", {})
        location = response.get("location", {})
        fraud_score = company.get("abuser_score", "").strip().split()
        fraud_score = fraud_score and fraud_score[0] or 0.0
        return cls(
            name='IPAPI',
            country=location.get("country", 'Unknown'),
            state=location.get("state", 'Unknown'),
            city=location.get("city", 'Unknown'),
            zip=location.get("zip", 'Unknown'),
            latitude=location.get("latitude", 0.0),
            longitude=location.get("longitude", 0.0),
            fraud_score=fraud_score,
            isp=company.get("name"),
            is_bogon=response.get("is_bogon"),
            is_mobile=response.get("is_mobile"),
            is_satellite=response.get("is_satellite"),
            is_crawler=response.get("is_crawler"),
            is_datacenter=response.get("is_datacenter"),
            is_tor=response.get("is_tor"),
            is_proxy=response.get("is_proxy"),
            is_vpn=response.get("is_vpn"),
            is_abuser=response.get("is_abuser"),
        )

class DBIP(BaseSource):
    @classmethod
    def from_response(cls, response: dict):
        info = response.get('demoInfo', {})
        return cls(
            name='DBIP',
            country=info.get('countryName', ''),
            state=info.get('stateProv', ''),
            city=info.get('city', ''),
            zip=info.get('zipCode'),
            latitude=info.get('latitude', 0.0),
            longitude=info.get('longitude', 0.0),
            fraud_score=info.get('threatLevel'),
            isp=info.get("isp"),
            is_crawler=info.get("isCrawler"),
            is_proxy=info.get("isProxy"),
        )

class IP2Location(BaseSource):
    @classmethod
    def from_response(cls, response: dict):
        proxy = response.get("proxy", {})
        return cls(
            name="IP2Location",
            country=response.get("country_name"),
            state=response.get("region_name"),
            city=response.get("city_name"),
            zip=response.get("zip_code"),
            latitude=response.get("latitude") or 0.0,
            longitude=response.get("longitude") or  0.0,
            fraud_score=response.get("fraud_score"),
            isp=response.get("isp"),
            is_crawler=proxy.get("is_web_crawler"),
            is_datacenter=proxy.get("is_data_center"),
            is_tor=proxy.get("is_tor"),
            is_proxy=response.get("is_proxy"),
            is_vpn=proxy.get("is_vpn"),
            is_spammer=proxy.get("is_spammer"),
            is_scanner=proxy.get("is_scanner"),
        )
