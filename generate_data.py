def generate_user():
    f = Faker()
    # Faker profile
    # user = User(first_name="Faker", last_name="Faker", username="faker", email="faker@faker.com")
    # user.set_password("testfaker")
    # user.save()

    profile = f.profile()
    user = User.objects.create(first_name=profile["name"].split()[0],
                               last_name=profile["name"].split()[1],
                               username=profile["username"],
                               email=profile["email"]
                               )
    user.set_password("hpenvy13")
    user.save()


def generate_post():
    f = Faker()

    for i in range(40):
        print(f"Creating post {i}...", end=" ")
        Post.objects.create(title=f.sentence(),
                            content=f.paragraph(),
                            is_active=True,
                            published=datetime.now().strftime("%Y-%m-%d"),
                            author_id=User.objects.get(id=random.choice([1, 2, 3, 4, 7, 8])).id
                            # data basedagi userlar id lariga asoslangan holda id lar tanlandi
                            )
        print("OK")


def main():
    # generate_user()
    generate_post()


if __name__ == "__main__":
    import os

    from django.core.wsgi import get_wsgi_application

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    application = get_wsgi_application()

    from django.utils.timezone import datetime
    import random
    from faker import Faker

    from blog.models import Post, User

    main()
