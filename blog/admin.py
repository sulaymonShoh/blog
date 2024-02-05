from django.contrib import admin

from blog.models import User, Post


# tabular inline or stacked inline
class PostInline(admin.StackedInline):
    model = Post
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [PostInline]
    list_display = ["first_name", "last_name", "username", "post_count", "password"]
    search_fields = ["first_name", "username", "last_name"]
    # list_filter = ["post_count",]
    list_display_links = ["username", "password"]

    def get_post_count(self):
        return self.post_count


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "author", "is_active", "published"]
    search_fields = ["title", "content"]
    list_filter = ["author", "is_active"]
    date_hierarchy = "published"
