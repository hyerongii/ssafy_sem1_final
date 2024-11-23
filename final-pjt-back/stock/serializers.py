from rest_framework import serializers
from .models import Theme, Stock, IndustryCode, UserProfile, Interest, Article, Comment

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class IndustryCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryCode
        fields = '__all__'

class ThemeSerializer(serializers.ModelSerializer):
    stocks = serializers.SerializerMethodField()
    industry_codes = IndustryCodeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Theme
        fields = '__all__'
    
    def get_stocks(self, obj):
        # stock_set에서 중복된 코드를 가진 주식 제거
        unique_stocks = {}
        for stock in obj.stock_set.all():
            if stock.code not in unique_stocks:
                unique_stocks[stock.code] = stock
        
        # 중복이 제거된 주식들을 직렬화
        return StockSerializer(unique_stocks.values(), many=True).data


class ThemeInfoSerializer(serializers.ModelSerializer):
    stocks = StockSerializer(source='stock_set', many=True, read_only=True)
    theme_name = serializers.CharField(source='name')
    
    class Meta:
        model = Theme
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class AnalyzeResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    recommended_themes = ThemeInfoSerializer(many=True)    

class ArticleSerializer(serializers.ModelSerializer):
    like_article = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    author = serializers.ReadOnlyField(source='author.nickname')
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.objects.all())
    theme = serializers.PrimaryKeyRelatedField(queryset=Theme.objects.all())
    
    class Meta:
        model = Article
        fields = (
            'id',
            'stock',
            'theme',
            'author',
            'title',
            'content',
            'created_at',
            'updated_at',
            'like_article'
        )
        read_only_fields = ('theme', 'like_article', 'author')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.nickname')
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'article',
            'stock',
            'theme',
            'user',
            'content',
            'created_at',
            'like_comment'
        )
        read_only_fields = (
            'article',
            'stock',
            'theme',
            'user',
            'created_at',
            'like_comment'
        )