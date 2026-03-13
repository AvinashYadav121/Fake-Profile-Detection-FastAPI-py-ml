from database import cursor, conn

def save_feedback(data):

    query = """
    INSERT INTO feedback_data (
        username,
        followers,
        following,
        posts,
        followers_following_ratio,
        bio_length,
        bio_has_link,
        username_digit_count,
        account_age_days,
        is_private,
        highlight_count,
        has_profile_pic,
        profile_image_face_detected,
        model_prediction,
        user_feedback,
        image_path
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, (

        data["username"],
        data["followers"],
        data["following"],
        data["posts"],

        data["followers_following_ratio"],

        data["bio_length"],
        data["bio_has_link"],
        data["username_digit_count"],

        data["account_age_days"],
        data["is_private"],
        data["highlight_count"],

        data["has_profile_pic"],
        data["profile_image_face_detected"],

        data["model_prediction"],
        data["user_feedback"],

        data["image_path"]

    ))

    conn.commit()