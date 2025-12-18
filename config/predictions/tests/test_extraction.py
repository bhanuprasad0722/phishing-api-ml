from ml.feature_extraction import extract_features,FEATURE_NAMES

def vector_len_of_features(): # checking the len of features and cols are same or not
    url = "https://google.com"
    features = extract_features(url)

    assert len(features) == len(FEATURE_NAMES)

def values_are_numeric(): # check if all the values are numeric or not
    url = "http://login-paypal.com/secure"
    features = extract_features(url)

    for value in features:
        assert isinstance(value,(int,float))

def test_https_feature():
    https_url = "https://example.com"
    http_url = "http://example.com"

    https_features = extract_features(https_url)
    http_features = extract_features(http_url)

    https_index = FEATURE_NAMES.index("has_https")

    assert https_features[https_index] == 1
    assert http_features[https_index] == 0
