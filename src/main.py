import asyncio

from checkers import IPChecker
from sources import BaseSource


def get_fraud(sources):
    names = [s.name for s in sources]
    max_len = max(len(n) for n in names)
    lines = ["Fraud scores:"]

    for s in sources:
        if s.fraud_score is not None:
            lines.append(f"{s.name:<{max_len}} - {s.fraud_score}")

    return "\n".join(lines)

def get_info(sources):
    fields = ["country", "state", "city", "zip", "latitude", "longitude"]

    results = {}
    for field in fields:
        results[field] = {}
        for source in sources:
            if value := getattr(source, field, None):
                if value in results[field]:
                    results[field][value].append(source.name)
                else:
                    results[field][value] = [source.name]

    lines = []
    for field, values in results.items():
        lines.append(f"\n{field.capitalize()}:")
        for value, sources in values.items():
            lines.append(f"{value:<10}: {', '.join(sources)}")

    return "\n".join(lines)


async def get_ip_info(sources: list):
    sources = [BaseSource(**s) if isinstance(s, dict) else s for s in sources]
    lines = []

    lines.append(get_fraud(sources))
    lines.append(get_info(sources))

    return "\n".join(lines)


async def main():
    data = await IPChecker('8.8.8.8').check()
    print(await get_ip_info(data.values()))


if __name__ == '__main__':
    asyncio.run(main())
