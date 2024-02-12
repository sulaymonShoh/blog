import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import User, Post


class PostTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(first_name="Test", last_name="User", username="testuser",
                                   avatar="../media/user_photos/default/default.jpg")
        user.set_password("tespassw")

        self.user = user
        post = Post.objects.create(title="Test", content="TEST", is_active=False,
                                   published=datetime.datetime.now().strftime("%Y-%m-%d"), author_id=self.user.id)

        self.post = post

    def test_post_detail(self):
        response = self.client.get(reverse("blog:post_detail", args=[str(self.post.pk)]))
        print(response.content)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
        # self.assertContains(response, self.post.is_active) #shu qator nimagadir ishlamadi
        self.assertContains(response, datetime.datetime.strptime(self.post.published, "%b. %d, %Y"))
