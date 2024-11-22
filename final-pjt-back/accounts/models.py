from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class InvestmentPeriod(models.TextChoices):
        SHORT_TERM = 'short', '단기'
        MEDIUM_TERM = 'medium', '중기'
        LONG_TERM = 'long', '장기'
    nickname = models.CharField(max_length=50)
    email = models.EmailField(blank=False)
    # token = models.TextField()
    
    # period = models.CharField(
    # max_length=6,
    # # 단기, 중기, 장기와 같은 투자 기간은 고정된 선택지
    # # 유저가 입력할 수 있는 값이 제한적이므로, ENUM을 사용하여 명확하게 정의할 수 있음.
    # # ENUM은 내부적으로 숫자로 저장되기 때문에 메모리 사용 측면에서도 효율적이다. 
    # # 예를 들어, "short", "medium", "long"을 각각 0, 1, 2로 저장할 수 있음.
    # # Django에서는 ENUM을 choices 옵션을 통해 구현할 수 있다. 
    # choices=InvestmentPeriod.choices,
    # default=InvestmentPeriod.SHORT_TERM,
    # )   
