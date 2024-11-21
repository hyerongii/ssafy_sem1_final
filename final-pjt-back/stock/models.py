from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mbti = models.CharField(max_length=4)
    period = models.CharField(max_length=10)
    token = models.TextField(null=True)

    def __str__(self):
        return self.user.username

class Theme(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    code = models.CharField(max_length=6)
    api_request_code = models.CharField(max_length=20, null=True, blank=True)
    industry_codes = models.ManyToManyField('IndustryCode', related_name='themes')

class Interest(models.Model):
    name = models.CharField(max_length=30)

class IndustryCode(models.Model):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    api_request_code = models.CharField(max_length=10)

class UserInterest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)


# class ChartPeriod(models.TextChoices):
#     DAY = 'D', '일'
#     WEEK = 'W', '주'
#     MONTH = 'M', '월'
#     YEAR = 'Y', '년'

# class ThemeChart(models.Model):
#     theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
#     period = models.CharField(
#         max_length=1,
#         choices=ChartPeriod.choices,
#         default=ChartPeriod.DAY
#     )
#     f_price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f'{self.theme.name} - {self.period}'

class Stock(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    description = models.TextField()
    price = models.IntegerField()
    excd = models.CharField(max_length=3,null=True)
    # Financial fields (예시로 추가된 필드들)
    per = models.DecimalField(max_digits=10, decimal_places=2)  # Price to Earnings Ratio
    pbr = models.DecimalField(max_digits=10, decimal_places=2)  # Price to Book Ratio
    consensus = models.CharField(max_length=50)  # Analyst consensus
    eps = models.DecimalField(max_digits=10, decimal_places=2)  # Earnings Per Share

    logo_img = models.TextField()
    def __str__(self):
        return self.name

# class StockChart(models.Model):
#     stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
#     current_price = models.FloatField()
#     date = models.DateTimeField(auto_now_add=True)
#     period = models.CharField(
#         max_length=1,
#         choices=ChartPeriod.choices,
#         default=ChartPeriod.DAY
#     )

#     def __str__(self):
#         return f'{self.stock.name} - {self.period}'

class Article(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=250)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_article = models.ManyToManyField(User, related_name='liked_articles')

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content = models.TextField(max_length=250)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    like_comment = models.ManyToManyField(User, related_name='liked_comments')

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'