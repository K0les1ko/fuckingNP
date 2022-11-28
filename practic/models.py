from django.db import models  # импорт
from django.contrib.auth.models import User
from django.db.models import Sum




#Модель Author
#Модель, содержащая объекты всех авторов.
#Имеет следующие поля:
#cвязь «один к одному» с встроенной моделью пользователей User;
#рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)
    name = models.CharField(max_length=120)

    def update_rating(self):
        postrat = self.post_set.aggregate(postRating=Sum('rating'))
        prat = 0
        prat += postrat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        crat = 0
        crat += commentRat.get('commentRating')

        self.rating = prat *3 + crat
        self.save()



#Модель Category
#Категории новостей/статей — темы, которые они отражают
# (спорт, политика, образование и т. д.). Имеет единственное поле: название категории.
# Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).

class Category(models.Model):
    cat_name = models.CharField(max_length=25, default=None)

    #Модель Post
#Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
# Каждый объект может иметь одну или несколько категорий.
#Соответственно, модель должна включать следующие поля:
#связь «один ко многим» с моделью Author;
#поле с выбором — «статья» или «новость»;
#автоматически добавляемая дата и время создания;
#связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
#заголовок статьи/новости;
#текст статьи/новости;
#рейтинг статьи/новости.


class Post(models.Model):  # наследуемся от класса Model
    header = models.CharField(max_length=255)
    pub_datetime = models.DateTimeField(auto_now_add=True)
    article_text = models.TextField()
    post = models.ForeignKey(Author, on_delete=models.CASCADE)
    cat_rel = models.ManyToManyField(Category, through="PostCategory")
    rating = models.IntegerField(default=0)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.article_text[0:123]


        #Модель PostCategory
#Промежуточная модель для связи «многие ко многим»:
#связь «один ко многим» с моделью Post;
#связь «один ко многим» с моделью Category.

class PostCategory(models.Model):
    post_rel = models.ForeignKey(Post, on_delete=models.CASCADE)
    cat_rel = models.ForeignKey(Category, on_delete=models.CASCADE)



#Модель Comment
#Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
#Модель будет иметь следующие поля:
#связь «один ко многим» с моделью Post;
#связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
#текст комментария;
#дата и время создания комментария;
#рейтинг комментария.

class Comment(models.Model):  # наследуемся от класса Model
    com_text = models.CharField(max_length=255)
    pub_datetime = models.DateTimeField(auto_now_add=True)
    user_relat = models.ForeignKey(User, on_delete=models.CASCADE)
    post_rela = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

