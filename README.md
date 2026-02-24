# Timeweb Cloud SDK <sub>via</sub> MewVPN

Минималистичный асинхронный Python SDK для работы с Timeweb Cloud API (v1).

Поддерживает управление серверами (on / off / reboot) и DNS.
Есть Builder API для создания серверов и DNS-записей.

## Установка

```bash
pip install git+https://github.com/yourname/timeweb-cloud-sdk.git
```

## Использование
```python
import asyncio
from timeweb_cloud_sdk import TimewebCloud

async def main():
    async with TimewebCloud(token="TOKEN") as client:
        servers = await client.servers.list()
        domains = await client.dns.list()

asyncio.run(main())
```
