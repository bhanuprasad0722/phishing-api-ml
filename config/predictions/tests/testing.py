from feature_extraction import extract_features, FEATURE_NAMES

url = "http://login-paypal.com/secure/update"
features = extract_features(url)

for name, value in zip(FEATURE_NAMES, features):
    print(f"{name}: {value}")