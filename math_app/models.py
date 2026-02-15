from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 学年モデル（中1〜高3）
class Grade(models.Model):
    
    GRADE_CHOICES = [
        ('junior1', '中学1年'),
        ('junior2', '中学2年'),
        ('junior3', '中学3年'),
        ('high1', '高校1年'),
        ('high2', '高校2年'),
        ('high3', '高校3年'),
    ]
    
    code = models.CharField(
        max_length=10,
        choices=GRADE_CHOICES,
        unique=True,
        verbose_name='学年コード'
    )
    
    name = models.CharField(
        max_length=20,
        verbose_name='学年名',
        help_text='例：中1, 高2など'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='表示順序'
    )
    
    class Meta:
        verbose_name = '学年'
        verbose_name_plural = '学年'
        ordering = ['order']
    
    def __str__(self):
        return self.name


# ユーザープロフィール（学年情報を管理）
class UserProfile(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='ユーザー'
    )
    
    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='学年'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='作成日時'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新日時'
    )
    
    class Meta:
        verbose_name = 'ユーザープロフィール'
        verbose_name_plural = 'ユーザープロフィール'
    
    def __str__(self):
        return f"{self.user.username} - {self.grade}"


# ==============================================================================
# 科目モデル（数I・A・II・B・III・C）
class Subject(models.Model):
    
    name = models.CharField(
        max_length=50,
        verbose_name='科目名',
        help_text='例：数1, 数A, 数2など'
    )
    
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name='学年',
        help_text='この科目が対応する学年（高1, 高2, 高3）'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='表示順序'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='作成日時'
    )
    
    class Meta:
        verbose_name = '科目'
        verbose_name_plural = '科目'
        ordering = ['grade', 'order', 'name']
    
    def __str__(self):
        return f"{self.name}"


# 学習単元タグモデル
class Tag(models.Model):
    """
    学習単元を表すタグモデル
    複数の Problem と Many-to-Many で紐付けられる
    
    属性：
    - name: タグ名（例：二次関数、確率、三角関数など）
    - grade: 学年（例：中1, 高2など）
    - subject: 科目（高校のみ）（例：数1, 数Aなど）
    """
    
    name = models.CharField(
        max_length=50,
        verbose_name='単元タグ',
        help_text='例：二次関数、確率、三角関数など'
    )
    
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tags',
        verbose_name='学年'
    )
    
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='tags',
        verbose_name='科目',
        help_text='高校の科目（高1～高3のみ）'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='習う順番',
        help_text='小さい数から大きい数の順に表示されます'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='作成日時'
    )
    
    class Meta:
        verbose_name = '単元タグ'
        verbose_name_plural = '単元タグ'
        ordering = ['grade', 'order', 'name']
        unique_together = ('name', 'grade')  # 同じ学年内では単元名は一意
    
    def __str__(self):
        return f"{self.grade} - {self.name}"


# 問題モデル（メイン）
class Problem(models.Model):
    
    # ユーザー（ForeignKey: ユーザー削除時に問題も削除）
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='problems',  # User.problems.all() で逆参照可能
        verbose_name='ユーザー'
    )
    
    # 学年（ForeignKey）
    grade = models.ForeignKey(
        Grade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='学年'
    )
    
    # 問題タイトル
    title = models.CharField(
        max_length=200,
        verbose_name='問題のタイトル',
        help_text='問題を簡潔に説明するタイトルを入力してください'
    )
    
    # 問題画像（media/problems/ に保存、任意）
    image = models.ImageField(
        upload_to='problems/',
        null=True,
        blank=True,
        verbose_name='問題の画像',
        help_text='問題の画像をアップロードしてください（手書きの場合、手書き画像を画像として保存できます）'
    )
    
    # ヒント1: 指針（解法の方針）
    hint_approach = models.TextField(
        blank=True,
        verbose_name='方針',
        help_text='問題を解くための方針や方向性を記入してください'
    )
    
    # ヒント1: 指針画像
    hint_approach_image = models.ImageField(
        upload_to='hints/approach/',
        null=True,
        blank=True,
        verbose_name='方針の画像',
        help_text='図や表などの画像をアップロードしてください'
    )
    
    # ヒント2: 検討（公式・定理）
    hint_formula = models.TextField(
        blank=True,
        verbose_name='公式',
        help_text='使用すべき公式や定理を記入してください'
    )
    
    # ヒント2: 公式画像
    hint_formula_image = models.ImageField(
        upload_to='hints/formula/',
        null=True,
        blank=True,
        verbose_name='公式の画像',
        help_text='公式や計算過程の画像をアップロードしてください'
    )
    
    # ヒント3: 注意点（ミスしやすい点）
    hint_technique = models.TextField(
        blank=True,
        verbose_name='コツ',
        help_text='計算や考え方のコツを記入してください'
    )
    
    # ヒント3: 注意点画像
    hint_technique_image = models.ImageField(
        upload_to='hints/technique/',
        null=True,
        blank=True,
        verbose_name='注意点の画像',
        help_text='重要なポイントの画像をアップロードしてください'
    )
    
    # 単元タグ（ManyToMany: 複数タグ可能）
    tags = models.ManyToManyField(
        Tag,
        related_name='problems',
        verbose_name='単元タグ',
        help_text='該当する単元タグを選択してください'
    )
    
    # 作成日時（自動記録）
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='投稿日時',
        help_text='問題が投稿された日時（自動で記録される）'
    )
    
    # 更新日時（自動更新）
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新日時',
        help_text='問題が最後に更新された日時（自動で更新される）'
    )
    
    class Meta:
        verbose_name = '数学の問題'
        verbose_name_plural = '数学の問題'
        ordering = ['-created_at']  # 最新順
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


# ヒントモデル（レガシー互換、現在は Problem 内に統合）
class Hint(models.Model):
    
    STAGE_CHOICES = (
        (0, '方針'),
        (1, '公式'),
        (2, 'コツ'),
    )
    
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='hints',
        verbose_name='関連する問題'
    )
    
    stage_type = models.IntegerField(
        choices=STAGE_CHOICES,
        default=0,
        verbose_name='ヒントの種類'
    )
    
    content = models.TextField(
        verbose_name='ヒントの内容'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='作成日時'
    )
    
    # =========================================================================
    # メタクラス：モデルの設定
    # =========================================================================
    class Meta:
        verbose_name = 'ヒント'
        verbose_name_plural = 'ヒント'
        ordering = ['problem', 'stage_type', 'created_at']
    
    def __str__(self):
        stage_name = dict(self.STAGE_CHOICES)[self.stage_type]
        return f"{self.problem.title} - {stage_name}"
    
    def get_stage_type_display_ja(self):
        return dict(self.STAGE_CHOICES).get(self.stage_type, '不明')


# ==============================================================================
# 質問モデル
# ==============================================================================
class Question(models.Model):
    """
    ユーザーから開発者への質問を管理
    """
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions',
        verbose_name='質問者'
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name='お名前'
    )
    
    email = models.EmailField(
        verbose_name='返信用メールアドレス'
    )
    
    subject = models.CharField(
        max_length=200,
        verbose_name='件名'
    )
    
    message = models.TextField(
        verbose_name='質問内容'
    )
    
    problem_image = models.ImageField(
        upload_to='questions/',
        null=True,
        blank=True,
        verbose_name='問題画像（任意）'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='送信日時'
    )
    
    is_replied = models.BooleanField(
        default=False,
        verbose_name='返信済み'
    )
    
    class Meta:
        verbose_name = '質問'
        verbose_name_plural = '質問'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
