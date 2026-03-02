import asyncio
import time
from typing import Dict

from .._http import HTTPClient
from .models import ARecord, CNAMERecord, dns_record_adapter
from .graph import DNSGraph


class DNSService:
    def __init__(self, http: HTTPClient, cache_ttl: int = 60):
        self._http = http
        self._cache_ttl = cache_ttl

        self._graph_cache: Dict[str, tuple[float, DNSGraph]] = {}
        self._locks: Dict[str, asyncio.Lock] = {}

    async def list_records(self, fqdn: str):
        data = await self._http.request(
            "GET",
            f"/domains/{fqdn}/dns-records",
        )

        return [dns_record_adapter.validate_python(r) for r in data.get("dns_records", [])]

    async def build_graph(self, fqdn: str) -> DNSGraph:
        now = time.time()

        cached = self._graph_cache.get(fqdn)
        if cached:
            created_at, graph = cached
            if now - created_at < self._cache_ttl:
                return graph

        lock = self._locks.setdefault(fqdn, asyncio.Lock())

        async with lock:
            cached = self._graph_cache.get(fqdn)
            now = time.time()

            if cached:
                created_at, graph = cached
                if now - created_at < self._cache_ttl:
                    return graph

            graph = await self._build_graph_internal(fqdn)
            self._graph_cache[fqdn] = (now, graph)

            return graph

    async def _build_graph_internal(self, fqdn: str) -> DNSGraph:
        records = await self.list_records_recursive(fqdn)
        graph = DNSGraph()

        for r in records:
            domain = r.full_name()

            if isinstance(r, ARecord):
                graph.add_a(domain, r.ip)

            elif isinstance(r, CNAMERecord):
                graph.add_cname(domain, r.target)

        return graph

    async def list_records_recursive(self, fqdn: str, _visited=None):
        if _visited is None:
            _visited = set()

        if fqdn in _visited:
            return []

        _visited.add(fqdn)

        records = await self.list_records(fqdn)
        all_records = list(records)

        for record in records:
            sub = getattr(record.data, "subdomain", None)

            if sub:
                sub_fqdn = f"{sub}.{fqdn}"

                if sub_fqdn not in _visited:
                    sub_records = await self.list_records_recursive(
                        sub_fqdn,
                        _visited,
                    )
                    all_records.extend(sub_records)

        return all_records

    async def find_domains_by_ip(self, fqdn: str, ip: str):
        graph = await self.build_graph(fqdn)
        return graph.domains_pointing_to_ip(ip)

    async def resolve(self, fqdn: str, domain: str):
        graph = await self.build_graph(fqdn)
        return graph.resolve(domain)

    async def impact_of_removal(self, fqdn: str, domain: str):
        graph = await self.build_graph(fqdn)
        return graph.impact_of_removal(domain)

    async def find_dangling(self, fqdn: str):
        graph = await self.build_graph(fqdn)
        return graph.find_dangling()

    def invalidate_cache(self, fqdn: str):
        self._graph_cache.pop(fqdn, None)
