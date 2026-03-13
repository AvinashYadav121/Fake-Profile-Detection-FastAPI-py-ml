
# from fastapi import APIRouter
# import psycopg2

# router = APIRouter()

# def get_db_connection():
#     return psycopg2.connect(
#         host="localhost",
#         database="fake_profile_db",
#         user="goku"
#     )


# @router.get("/admin/dashboard")
# def admin_dashboard():

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT id,
#                dataset,
#                final_model_prediction,
#                final_confidence,
#                user_label,
#                user_satisfied
#         FROM feedback_data
#         ORDER BY id DESC
#     """)

#     rows = cursor.fetchall()

#     data = []

#     for r in rows:
#         data.append({
#             "id": r[0],
#             "dataset": r[1],
#             "finalModelPrediction": r[2],
#             "finalConfidence": r[3],
#             "userLabel": r[4],
#             "userSatisfied": r[5]
#         })

#     cursor.close()
#     conn.close()

#     return data

