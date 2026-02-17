import instaloader

loader = instaloader.Instaloader()

def fetch_profile(username: str):
    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        return {
        "username": profile.username,
        "full_name": profile.full_name,
        "bio": profile.biography or "",
        "followers": profile.followers,
        "following": profile.followees,
        "posts": profile.mediacount,
        "is_private": profile.is_private,
        "is_verified": profile.is_verified,
        "has_pic": profile.profile_pic_url is not None,
        "profile_pic_url": str(profile.profile_pic_url)
    }


    except Exception as e:
        return None
