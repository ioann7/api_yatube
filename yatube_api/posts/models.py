from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        help_text='Введите заголовок группы',
        max_length=200
    )
    slug = models.SlugField(
        'slug',
        max_length=50,
        unique=True
    )
    description = models.TextField(
        'Описание',
        help_text='Введите описание группы'
    )

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        'Текст', help_text='Введите текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Картинка', upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', verbose_name='Группа',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
        help_text='Выберите пост к которому принадлежит комментарий'
    )
    text = models.TextField(
        'Текст', help_text='Введите текст комментария')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
        ordering = ('-created',)

    def __str__(self) -> str:
        return self.text[:10]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'follow'
        verbose_name_plural = 'follows'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='user_not_equal_following'
            )
        )
