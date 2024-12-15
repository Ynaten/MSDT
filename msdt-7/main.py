import asyncio
import aiohttp

# URL API для курсов валют
currency_url = "https://v6.exchangerate-api.com/v6/8c3923ee495342e7fd3399a6/latest/RUB"  # Замените на ваш реальный API-ключ

# Список популярных валют
popular_currencies = [
    'USD', 'EUR', 'GBP', 'AUD', 'CAD', 'JPY', 'CHF', 'CNY', 'INR', 'BRL', 'RUB'
]

# Асинхронная функция для получения курса валют
async def get_currency():
    async with aiohttp.ClientSession() as session:
        async with session.get(currency_url) as response:
            data = await response.json()
            if response.status == 200:
                return data["conversion_rates"]
            else:
                return None

# Функция для конвертации валют
async def convert_currency(amount, from_currency, to_currency, conversion_rates):
    if from_currency != "RUB":
        amount = amount / conversion_rates[from_currency]  # Преобразуем сумму в рубли

    # Конвертируем в целевую валюту
    converted_amount = amount * conversion_rates[to_currency]
    return round(converted_amount, 2)

# Асинхронная функция для выполнения конверсий в все популярные валюты
async def convert_to_popular_currencies(amount, from_currency, conversion_rates):
    tasks = []
    for to_currency in popular_currencies:
        if to_currency != from_currency:
            tasks.append(convert_currency(amount, from_currency, to_currency, conversion_rates))
    
    # Выполняем все задачи асинхронно
    results = await asyncio.gather(*tasks)
    
    return results

# Главная асинхронная функция
async def main():
    print("Добро пожаловать в конвертер валют!")
    
    # Запрашиваем валюту у пользователя
    print("Доступные валюты:")
    for currency in popular_currencies:
        print(currency)
    
    from_currency = input("\nВведите валюту, из которой конвертировать (например, USD, EUR): ").upper()

    # Запрашиваем сумму для конвертации
    amount = float(input("Введите сумму для конвертации: "))
    
    # Получаем курсы валют
    conversion_rates = await get_currency()
    
    if conversion_rates:
        # Конвертируем в 10 популярных валют
        results = await convert_to_popular_currencies(amount, from_currency, conversion_rates)
        
        # Выводим результаты
        print(f"\nКонвертация {amount} {from_currency} в другие популярные валюты:")
        for to_currency, result in zip(popular_currencies, results):
            if to_currency != from_currency:
                print(f"{amount} {from_currency} = {result} {to_currency}")
    else:
        print("Не удалось получить данные о курсах валют.")

# Запуск асинхронной программы
if __name__ == "__main__":
    asyncio.run(main())