"""Company website search using Google Custom Search API.

Requires environment variables:
  GOOGLE_CSE_API_KEY : API key for Google Custom Search
  GOOGLE_CSE_CX      : Custom search engine ID
"""

import os
import re
import requests
from typing import Optional


class CompanySearcher:
    """Search for a company website using Google Custom Search API."""

    EXCLUDE_DOMAINS = (
        "linkedin.com",
        "indeed.com",
        "glassdoor.com",
        "naukri.com",
        "internshala.com",
        "facebook.com",
        "twitter.com",
        "x.com",
    )

    def __init__(self) -> None:
        self.api_key = os.getenv("GOOGLE_CSE_API_KEY")
        self.cx = os.getenv("GOOGLE_CSE_CX")

    def search_company(self, company_name: str) -> Optional[str]:
        """Return the best-guess official website URL for the company."""
        if not self.api_key or not self.cx:
            raise RuntimeError("Google CSE API key or CX not configured")

        query = f"{company_name} official website"
        params = {
            "key": self.api_key,
            "cx": self.cx,
            "q": query,
            "num": 5,
        }

        resp = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        items = data.get("items", [])
        if not items:
            return None

        cleaned = self._filter_results(items, company_name)
        return cleaned[0] if cleaned else items[0].get("link")

    def _filter_results(self, items, company_name: str):
        company_slug = re.sub(r"[^a-z0-9]", "", company_name.lower())
        results = []
        for item in items:
            link = item.get("link", "")
            display = item.get("displayLink", "")
            if not link:
                continue

            # Skip common job boards / socials
            if any(excl in link for excl in self.EXCLUDE_DOMAINS):
                continue

            # Prefer domains whose root contains company slug
            if company_slug and company_slug in display.replace(".", ""):
                results.append(link)
                continue

            # Otherwise keep as fallback
            results.append(link)
        return results