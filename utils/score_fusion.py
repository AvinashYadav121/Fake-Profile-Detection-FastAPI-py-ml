def combine_scores(tabular_score, image_score, profile):

    bonus = 0

    has_pic = profile.get("has_pic", False)
    bio = profile.get("bio", "")
    is_verified = profile.get("is_verified", False)
    is_private = profile.get("is_private", False)

    if not has_pic:
        bonus += 0.1

    if len(bio) < 5:
        bonus += 0.05

    if is_private:
        bonus += 0.08

    if is_verified:
        bonus -= 0.15

    final = (tabular_score * 0.65) + (image_score * 0.35) + bonus

    return min(max(final, 0), 1.0)


def detect_impersonation(profile, image_score):

    if (
        image_score > 0.7 and
        profile.get("followers", 0) < 5000 and
        not profile.get("is_verified", False)
    ):
        return True

    return False


def explain_profile(profile, tabular_score, image_score):

    reasons = []

    if profile.get("followers",0) < 50:
        reasons.append("Very low followers")

    if profile.get("posts",0) < 3:
        reasons.append("Low number of posts")

    if not profile.get("has_pic",False):
        reasons.append("No profile picture")

    if len(profile.get("bio","")) < 5:
        reasons.append("Bio missing")

    if profile.get("is_private",False):
        reasons.append("Private account hides activity")

    if image_score > 0.6:
        reasons.append("Suspicious profile image")

    if tabular_score > 0.6:
        reasons.append("Behaviour pattern looks fake")

    if detect_impersonation(profile, image_score):
        reasons.append("Possible celebrity impersonation")

    return reasons
