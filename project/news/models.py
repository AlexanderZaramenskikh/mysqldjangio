from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = 0
        comment_rating = 0
        post_comment_rating = 0

        posts = Post.objects.filter(one_to_many_relation=self)
        for p in posts:
            post_rating += p.post_rating
        comments = Comment.objects.filter(one_to_many_relation1=self.user)
        for c in comments:
            comment_rating += c.comment_rating
        post_comment = Comment.objects.filter(one_to_many_relation_posts__one_to_many_relation=self)
        for pc in post_comment:
            post_comment_rating += pc.comment_rating

        self.rating = post_rating * 3 + comment_rating + post_comment_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=100)


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    POSITIONS = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    one_to_many_relation = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice = models.CharField(max_length=2, choices=POSITIONS, default=news)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    post_rating = models.IntegerField(default=0)

    def preview(self):
        return self.content[0:124] + "..."

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    one_to_many_relation = models.ForeignKey(Post, on_delete=models.CASCADE)
    one_to_many_relation1 = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    one_to_many_relation_posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    one_to_many_relation1 = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    date_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

