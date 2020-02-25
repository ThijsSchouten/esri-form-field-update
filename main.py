import re
import copy

from pprint import pprint

from arcgisonline_uitls import get_token, query_features, update_features
from config import pw, un


def main():

    service_url = r"https://services.arcgis.com/170JHtnttvl7hYmM/ArcGIS/rest/services/service_703ddb35fc604e47b2c800c288003247/FeatureServer/0"

    # Test

    token = get_token(un, pw)

    # Dict with all features
    original_features = query_features(service_url, token)
    features = copy.deepcopy(original_features)

    # Update fields to readable text
    for i, feature in enumerate(features):
        for key in features[i]["attributes"]:
            pretty_string = prettify(features[i]["attributes"][key])
            features[i]["attributes"][key] = pretty_string

    # Track changes
    for original, edited in zip(original_features, features):
        if original.items() == edited.items():
            print("Pass -> Nothing changed")
            continue
        else:
            print("Update features")
            print(update_features(service_url, token, edited))


def prettify(s):
    """
    ToDo: properly learn regex..
    """

    if isinstance(s, str):
        s = re.sub(r"_,", ",", s)  # Underscore + comma = comma
        s = re.sub(r"_", r" ", s)  # Underscore = whitespace
        s = re.sub(
            r",+", ", ", s
        )  # Comma + multiple whitespace = comma + single whitespace
        s = re.sub(r" ,", ",", s)  # Remove leading whitespace before comma
        s = re.sub(r" +", " ", s)  # Replace multple whitespace with single
        s = s.lstrip().rstrip()
        return s
    else:
        return s


if __name__ == "__main__":
    main()
