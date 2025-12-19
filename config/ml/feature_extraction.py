import re
from urllib.parse import urlparse

SUSPICIOUS_KEY_WORDS = [
    "login", "signin", "account", "verify", "secure", "update", "bank"
]

SHORTENING_SERVICES = [
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd"
]

SUSPICIOUS_TLDS = [
    ".zip", ".tk", ".ml", ".ga", ".cf"
]


def extract_features(url: str):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    query = parsed.query

    # Fix: add http scheme if missing
    if not domain:
        if url.startswith("http://") or url.startswith("https://"):
            domain = parsed.netloc
        else:
            url = "http://" + url
            parsed = urlparse(url)
            domain = parsed.netloc

    # If still empty, raise error
    if not domain:
        raise ValueError(f"Cannot extract domain from URL: {url}")

    features = [
        len(url),  # length
        url.count("."),  # num of dots
        len(re.findall(r'\d', url)),  # num of digits
        domain.count("-"),  # num of - in domain
        len(re.findall(r"[/&?=]", url)),  # num of special characters
        1 if "@" in url else 0,  # presence of @ 
        1 if parsed.scheme == "https" else 0,  # https used or not
        domain.count(".") - 1 if domain.count(".") > 0 else 0,  # num of subdomain
        len(domain),
        1 if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", domain) else 0,  # IP address usage instead of domain
        1 if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS) else 0,  # suspicious TLD
        sum(keyword in url.lower() for keyword in SUSPICIOUS_KEY_WORDS),  # suspicious keywords
        1 if any(service in domain for service in SHORTENING_SERVICES) else 0,  # URL shortener
        len(query.split("&")) if query else 0,  # num of query params
    ]
    return features



FEATURE_NAMES = [
    "url_length",
    "num_dots",
    "num_digits",
    "num_hyphens",
    "special_char_count",
    "has_at_symbol",
    "has_https",
    "num_subdomains",
    "domain_length",
    "uses_ip_address",
    "suspicious_tld",
    "suspicious_keywords",
    "url_shortener",
    "num_query_params",
]
