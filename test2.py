from itertools import islice
import mysql.connector

from instaloader import Instaloader, Profile

# =mysql://sace4948_blog:bloG123$%&@109.234.161.154:3306/sace4948_blogbloom?connection_limit=5&socket_timeout=9
db = mysql.connector.connect(
    host="109.234.161.154",
    port="3306",
    user="sace4948_blog",
    password="bloG123$%&",
    database="sace4948_blogbloom",
)
cursor = db.cursor()

query = (
    "SELECT first_name, last_name, hire_date FROM employees "
    "WHERE hire_date BETWEEN %s AND %s"
)


PROFILE = "bloom_family_travel"  # profile to download from

L = Instaloader()


profile = Profile.from_username(L.context, PROFILE)

for post in profile.get_posts():
    # print(post.owner_id)
    # print(post.video_url)
    print(post.mediaid)
    # print(post.shortcode)
    # print(post.url)  # thumbnail
    # print(post.caption)

    querySelect = "select * from posts where mediaId ='" + str(post.mediaid) + "';"
    cursor.execute(querySelect)
    recordPost = cursor.fetchone()
    db.commit()
    idTypePost = 4  # image
    if recordPost:
        cursor.execute(
            "UPDATE posts SET (`contentHtml`=%s, `mainMedia`=%s, `types_id`=%s, `published`=%s, `description`=%s, `imagePreview`=%s, `redirectTo`=%s, `title`=%s) WHERE mediaId=%s",
            (
                post.caption,
                post.url,
                idTypePost,
                1,
                "instagram migration",
                post.url,
                "",
                post.title,
                post.mediaid,
            ),
        )
        db.commit()
    else:
        if post.is_video:
            idTypePost = 2
        cursor.execute(
            "INSERT INTO posts (`contentHtml`, `mainMedia`, `types_id`, `published`, `description`, `imagePreview`, `redirectTo`, `title`, mediaId) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s);",
            (
                post.caption,
                post.url,
                idTypePost,
                1,
                "instagram migration",
                post.url,
                "",
                post.title,
                str(post.mediaid),
            ),
        )
        db.commit()
        querySelect = "select * from posts where mediaId ='" + str(post.mediaid) + "';"
        cursor.execute(querySelect)
        recordPost = cursor.fetchone()
        db.commit()
    for children in post.get_sidecar_nodes():
        querySelect = (
            "select * from images where url ='" + str(children.display_url) + "';"
        )
        cursor.execute(querySelect)
        recordImage = cursor.fetchone()
        db.commit()
        if recordImage:
            print(recordImage)
        else:
            print(recordImage)
            cursor.execute(
                "INSERT INTO images (`url`, `posts_Id`, `is_video`) VALUES (%s, %s, %s);",
                (children.display_url, recordPost[0], children.is_video),
            )
            db.commit()

    # L.download_post(post, PROFILE) */
cursor.close()
db.close()
