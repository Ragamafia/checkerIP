import asyncio

from checkers import IPChecker


async def main(ip):
    data = await IPChecker(ip).check()
    print(data)
    for i in data.values():
        print(i)


if __name__ == '__main__':
    ip = input('Enter IP-address: ')
    asyncio.run(main(ip))
