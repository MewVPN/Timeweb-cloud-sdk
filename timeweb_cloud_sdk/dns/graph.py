from collections import defaultdict
from typing import Dict, Set, List


class DNSGraph:
    def __init__(self):
        self.a_records: Dict[str, str] = {}
        self.cname_records: Dict[str, str] = {}
        self.reverse_ip_index: Dict[str, Set[str]] = defaultdict(set)

        self.dependencies: Dict[str, Set[str]] = defaultdict(set)

    def add_a(self, domain: str, ip: str):
        self.a_records[domain] = ip
        self.reverse_ip_index[ip].add(domain)

    def add_cname(self, domain: str, target: str):
        self.cname_records[domain] = target
        self.dependencies[target].add(domain)

    def resolve(self, domain: str) -> str | None:
        visited = set()

        while domain in self.cname_records:
            if domain in visited:
                return None
            visited.add(domain)
            domain = self.cname_records[domain]

        return self.a_records.get(domain)

    def domains_pointing_to_ip(self, ip: str) -> Set[str]:
        result = set(self.reverse_ip_index.get(ip, set()))

        for domain in self.cname_records:
            if self.resolve(domain) == ip:
                result.add(domain)

        return result

    def dependents(self, domain: str) -> Set[str]:
        return self.dependencies.get(domain, set())

    def impact_of_removal(self, domain: str) -> Set[str]:
        impacted = set()
        stack = [domain]

        while stack:
            current = stack.pop()
            for dep in self.dependencies.get(current, []):
                if dep not in impacted:
                    impacted.add(dep)
                    stack.append(dep)

        return impacted

    def find_dangling(self) -> List[str]:
        broken = []

        for domain in self.cname_records:
            if self.resolve(domain) is None:
                broken.append(domain)

        return broken
