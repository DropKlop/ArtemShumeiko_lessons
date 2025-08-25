import asyncio


async def get_data_async(args):
    print(f"Параметры получены {args}")
    if args == "Дубай":
        await asyncio.sleep(2)
    elif args == "Сочи":
        await asyncio.sleep(4)
    print(f"Данные получены {args}")

async def main():
    task = [
        get_data_async("Дубай"),
        get_data_async("Дубай"),
        get_data_async("Дубай"),
        get_data_async("Дубай"),
        get_data_async("Дубай"),
        get_data_async("Дубай"),
        get_data_async("Сочи")
            ]
    tk = await asyncio.gather(*task)

asyncio.run(main())