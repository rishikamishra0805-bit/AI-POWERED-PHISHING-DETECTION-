import re
from urllib.parse import urlparse

def extract_features(url):
    features = [0] * 30

    parsed = urlparse(url)

    # 1. URL length
    features[0] = len(url)

    # 2. HTTPS
    features[1] = 1 if parsed.scheme == "https" else -1

    # 3. @ symbol
    features[2] = -1 if "@" in url else 1

    # 4. Number of dots
    features[3] = url.count(".")

    # 5. URL has IP address
    if re.match(r"^(http://|https://)?\d+\.\d+\.\d+\.\d+", url):
        features[4] = -1
    else:
        features[4] = 1

    # 6. Hyphen in domain
    features[5] = -1 if "-" in parsed.netloc else 1

    # 7. Number of digits
    features[6] = sum(c.isdigit() for c in url)

    # 8. Special characters
    features[7] = sum(not c.isalnum() for c in url)

    # Remaining features (default safe value)
    for i in range(8, 30):
        features[i] = 1

    return features