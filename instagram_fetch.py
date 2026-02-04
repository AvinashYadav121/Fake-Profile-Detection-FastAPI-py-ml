# import instaloader

# L = instaloader.Instaloader()

# def fetch_instagram_profile(username: str):
#     profile = instaloader.Profile.from_username(L.context, username)

#     data = {
#         "followers": profile.followers,
#         "following": profile.followees,
#         "posts": profile.mediacount,
#         "is_private": int(profile.is_private),
#         "has_external_url": int(bool(profile.external_url)),
#         "bio_length": len(profile.biography or ""),
#         "username_length": len(profile.username),
#         "username_has_number": int(any(char.isdigit() for char in profile.username)),
#         "profile_pic": int(profile.profile_pic_url is not None)
#     }

#     return data


import instaloader

# Initialize Instaloader
L = instaloader.Instaloader()

# ---------------------------
# Fetch Instagram profile
# ---------------------------
def fetch_instagram_profile(username: str):
    profile = instaloader.Profile.from_username(L.context, username)

    data = {
        "followers": profile.followers,
        "following": profile.followees,
        "posts": profile.mediacount,
        "is_private": int(profile.is_private),
        "has_external_url": int(bool(profile.external_url)),
        "bio_length": len(profile.biography or ""),
        "username_length": len(profile.username),
        "username_has_number": int(any(c.isdigit() for c in profile.username)),
        "profile_pic": int(profile.profile_pic_url is not None),
        "full_name_length": len(profile.full_name or ""),
        "full_name_has_number": int(any(c.isdigit() for c in profile.full_name or ""))
    }

    return data


# ---------------------------
# MAP → DATASET 1 FEATURES
# ---------------------------
def map_to_dataset1(insta):
    """
    Order MUST match training:
    [
      edge_followed_by,
      edge_follow,
      username_length,
      username_has_number,
      full_name_has_number,
      full_name_length,
      is_private,
      is_joined_recently,
      has_channel,
      is_business_account,
      has_guides,
      has_external_url
    ]
    """
    return [
        insta["followers"],                 # edge_followed_by
        insta["following"],                 # edge_follow
        insta["username_length"],
        insta["username_has_number"],
        insta["full_name_has_number"],
        insta["full_name_length"],
        insta["is_private"],
        0,                                  # is_joined_recently (unknown)
        0,                                  # has_channel
        0,                                  # is_business_account
        0,                                  # has_guides
        insta["has_external_url"]
    ]


# ---------------------------
# MAP → DATASET 2 FEATURES
# ---------------------------
def map_to_dataset2(insta):
    """
    Order MUST match training:
    [
      profile pic,
      nums/length username,
      fullname words,
      nums/length fullname,
      name==username,
      description length,
      external URL,
      private,
      #posts,
      #followers,
      #follows
    ]
    """
    username_num_ratio = (
        insta["username_has_number"] / max(insta["username_length"], 1)
    )

    return [
        insta["profile_pic"],
        username_num_ratio,
        0,                                  # fullname words (not available)
        0,                                  # nums/length fullname
        0,                                  # name==username
        insta["bio_length"],
        insta["has_external_url"],
        insta["is_private"],
        insta["posts"],
        insta["followers"],
        insta["following"]
    ]
