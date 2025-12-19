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
    """
    Always returns a fixed-length numeric feature vector (14 features)
    """

    if not url or not isinstance(url, str):
        return [0] * 14

    # Ensure scheme exists (VERY IMPORTANT)
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path
    query = parsed.query

    features = [
        len(url),                                     # 0 url length
        url.count("."),                               # 1 number of dots
        len(re.findall(r"\d", url)),                  # 2 number of digits
        domain.count("-"),                            # 3 hyphens in domain
        len(re.findall(r"[/&?=]", url)),              # 4 special characters
        1 if "@" in url else 0,                       # 5 @ symbol
        1 if parsed.scheme == "https" else 0,         # 6 https used
        max(domain.count(".") - 1, 0),                # 7 subdomains
        len(domain),                                  # 8 domain length
        1 if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", domain) else 0,  # 9 IP usage
        1 if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS) else 0,  # 10 TLD
        sum(k in url.lower() for k in SUSPICIOUS_KEY_WORDS),  # 11 keywords
        1 if any(s in domain for s in SHORTENING_SERVICES) else 0,  # 12 shortener
        len(query.split("&")) if query else 0          # 13 query params
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
