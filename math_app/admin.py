from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Problem, Tag, Hint, Grade, UserProfile, Subject, Question, Question


# ==============================================================================
# UserProfile Adminクラス
# ==============================================================================
class UserProfileInline(admin.StackedInline):
    """
    User に紐付く UserProfile を inline で編集
    """
    model = UserProfile
    can_delete = False
    fields = ('grade',)


# User Admin の拡張
class CustomUserAdmin(BaseUserAdmin):
    """
    Django のデフォルト User Admin を拡張
    UserProfile をinlineで管理できるようにする
    """
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'get_grade', 'is_staff', 'is_active')
    list_select_related = ('profile', 'profile__grade')

    def get_grade(self, obj):
        """ユーザーの学年を表示"""
        if hasattr(obj, 'profile') and obj.profile and obj.profile.grade:
            return obj.profile.grade.name
        return '-'

    get_grade.short_description = '学年'


# User Admin を再登録
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# ==============================================================================
# Subject Adminクラス
# ==============================================================================
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Subject モデルの Admin カスタマイズ
    高校の科目（数1, 数A, 数2など）を管理
    """
    
    list_display = ('name', 'grade', 'order', 'get_tag_count')
    list_filter = ('grade',)
    search_fields = ('name', 'grade__name')
    ordering = ('grade', 'order', 'name')
    readonly_fields = ('created_at',)
    fields = ('name', 'grade', 'order', 'created_at')
    
    def get_tag_count(self, obj):
        """この科目に含まれる単元の数"""
        return obj.tags.count()
    
    get_tag_count.short_description = '単元数'


# ==============================================================================
# Tag Adminクラス
# ==============================================================================
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Tag モデルの Admin カスタマイズ
    学習単元（タグ）を管理
    """
    
    list_display = ('name', 'grade', 'subject', 'order', 'get_problem_count', 'created_at')
    list_filter = ('grade', 'subject', 'created_at')
    search_fields = ('name', 'grade__name', 'subject__name')
    ordering = ('grade', 'subject', 'order', 'name')
    readonly_fields = ('created_at',)
    fields = ('grade', 'subject', 'order', 'name', 'created_at')
    
    def get_problem_count(self, obj):
        """このタグに紐付く問題の数"""
        return obj.problems.count()
    
    get_problem_count.short_description = '問題数'


# ==============================================================================
# Problem Adminクラス
# ==============================================================================
@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    """
    Problem モデルの Admin カスタマイズ
    セルフ・アウトプット型学習用の問題管理
    """
    
    # =========================================================================
    # リスト表示設定
    # =========================================================================
    list_display = (
        'title',
        'user',
        'grade',
        'get_tags',
        'created_at',
        'updated_at'
    )
    
    list_filter = (
        'created_at',
        'updated_at',
        'user',
        'grade',
        'tags'
    )
    
    search_fields = (
        'title',
        'hint_approach',
        'hint_formula',
        'hint_technique',
        'user__username'
    )
    
    ordering = ('-created_at',)
    list_per_page = 25
    
    # =========================================================================
    # 詳細ページ設定
    # =========================================================================
    fieldsets = (
        ('基本情報', {
            'fields': ('user', 'grade', 'title', 'image')
        }),
        
        ('セルフ・アウトプット（ヒント）', {
            'fields': ('hint_approach', 'hint_formula', 'hint_technique'),
            'description': 'ユーザーが自分で入力したヒント情報'
        }),
        
        ('単元タグ', {
            'fields': ('tags',)
        }),
        
        ('投稿情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    filter_horizontal = ('tags',)
    
    # =========================================================================
    # カスタム表示メソッド
    # =========================================================================
    def get_tags(self, obj):
        """このProblemに紐付くタグを表示"""
        tags = obj.tags.all()
        if tags:
            return ', '.join([tag.name for tag in tags])
        return '-'
    
    get_tags.short_description = 'タグ'


# ==============================================================================
# Hint Adminクラス
# ==============================================================================
@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    """
    Hint モデルの Admin カスタマイズ
    レガシー互換（今後は使用しない予定）
    """
    
    list_display = (
        'problem',
        'get_stage_type',
        'content_preview',
        'created_at'
    )
    
    list_filter = (
        'stage_type',
        'created_at',
        'problem__user'
    )
    
    search_fields = (
        'problem__title',
        'content'
    )
    
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('ヒント情報', {
            'fields': ('problem', 'stage_type', 'content')
        }),
        
        ('投稿情報', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_stage_type(self, obj):
        """ヒント種類を日本語で表示"""
        return obj.get_stage_type_display()
    
    get_stage_type.short_description = 'ヒント種類'
    
    def content_preview(self, obj):
        """ヒント内容をプレビュー表示"""
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content
    
    content_preview.short_description = 'ヒント内容'


# ==============================================================================
# Question Adminクラス
# ==============================================================================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Question モデルの Admin カスタマイズ
    """
    list_display = ('id', 'name', 'email', 'subject', 'is_replied', 'created_at')
    list_filter = ('is_replied', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('質問者情報', {
            'fields': ('user', 'name', 'email')
        }),
        
        ('質問内容', {
            'fields': ('subject', 'message', 'problem_image')
        }),
        
        ('管理情報', {
            'fields': ('is_replied', 'created_at')
        }),
    )
    
    def has_add_permission(self, request):
        """管理画面から質問の追加は不可"""
        return False
