# proxy_generator/proxy.py
import requests
import re
import random

def fetch_proxies() -> list[str]:
    """
    Получение списка прокси из веб-источника без использования BeautifulSoup.
    
    :return: Список прокси в формате "IP:PORT".
    """
    url = "https://www.free-proxy-list.net/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Не удалось получить прокси.")
        return []
    
    # Используем регулярные выражения для поиска IP и PORT
    proxies = re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)', response.text)

    # Удаляем дубликаты и возвращаем уникальные прокси
    return list(set(proxies))

def validate_proxy(proxy: str) -> bool:
    """
    Проверка валидности прокси.

    :param proxy: Прокси в формате "IP:PORT".
    :return: True, если прокси валиден, иначе False.
    """
    try:
        # Попытка выполнить запрос через прокси
        response = requests.get("http://httpbin.org/ip", proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

def generate_proxies(country: str, quantity: int) -> list[str]:
    """
    Генерация списка прокси на основе выбранной страны.
    
    :param country: Страна, для которой генерируются прокси (на данный момент не используется).
    :param quantity: Количество прокси для генерации.
    :return: Список сгенерированных прокси.
    """
    # Получаем прокси из источника
    all_proxies = fetch_proxies()
    
    # Возвращаем случайные прокси из списка
    return random.sample(all_proxies, min(quantity, len(all_proxies)))
