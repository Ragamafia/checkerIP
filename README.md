IP чекер.
Этот код предназначен для проверки безопасности заданного IP-адреса.
Программа получает конкретный IP и выполняет его проверку на пяти различных ресурсах. IPInfo, IPAPI, DBIP, IP2Location и ScamAlytics. Она асинхронно обращается к сайтам, собирает информацию с помощью парсеров на базе BeautifulSoup, использует aiohttp для асинхронных запросов и fake_useragent для генерации случайных заголовков. В результате выводит собранные данные в формате JSON или текстовом виде.

Структура проекта
main.py — точка входа

checkers.py — основной скрипт, реализующий логику проверки и взаимодействия с ресурсами.

sources.py — содержит определения классов и схем данных с использованием pydantic.

Используемые технологии:

aiohttp — асинхронные HTTP-запросы 
BeautifulSoup — парсинг HTML-страниц 
fake-useragent — генерация случайных User-Agent
pydantic — валидация и структура данных
asyncio — управление асинхронными задачами

Установка
Для запуска проекта потребуется установить зависимости указанные в requirements.txt (pip install -r requirements.txt)
Для стабильного соединения вам потребуется прокси (config -> DEFAULT_PROXY)

Запуск скрипта: python main.py -> ввод IP 
Скрипт отдает словарь содержащий полную информацию о введенном IP. 

______________________________________________________________________

IP Checker

This code is designed to verify the security of a specified IP address. The program takes a specific IP and performs checks across five different resources: IPInfo, IPAPI, DBIP, IP2Location, and ScamAlytics. It asynchronously makes requests to these sites, collects information using parsers based on BeautifulSoup, utilizes aiohttp for asynchronous requests, and fake_useragent to generate random headers. As a result, it outputs the collected data in JSON format or as plain text.

Project Structure
main.py — entry point
checkers.py — main script implementing the checking logic and resource interaction
sources.py — contains class definitions and data schemas using pydantic

Technologies Used
aiohttp — asynchronous HTTP requests
BeautifulSoup — HTML page parsing
fake-useragent — generating random User-Agent headers
pydantic — data validation and structuring
asyncio — managing asynchronous tasks

Installation
To run the project, install dependencies listed in requirements.txt:
pip install -r requirements.txt

Running the script: python main.py -> enter IP 
