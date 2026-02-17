import re
import math

def extract_features(profile):

    username = profile["username"]
    followers = profile["followers"]
    following = profile["following"]
    posts = profile["posts"]
    bio = profile["bio"]

    digit_count = sum(c.isdigit() for c in username)

    username_length = len(username)
    bio_length = len(bio)

    follow_ratio = following / (followers + 1)
    engagement_proxy = posts / (followers + 1)
    digit_density = digit_count / (username_length + 1)

    bio_presence = 1 if bio_length > 5 else 0

    return [
        followers,
        following,
        posts,
        bio_length,
        int(profile["is_private"]),
        int(profile["has_pic"]),
        follow_ratio,
        engagement_proxy,
        digit_density,
        bio_presence
    ]
