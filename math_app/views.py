# Django Views：問題のCRUD処理
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Problem, Hint, Tag, Grade, UserProfile, Subject, Question
from .forms import CustomUserCreationForm, QuestionForm

logger = logging.getLogger(__name__)


# トップページ
def index(request):
    return render(request, 'math_app/index.html')


# 問題作成（CreateView）
class ProblemCreateView(LoginRequiredMixin, CreateView):
    """新しい数学問題を作成"""
    model = Problem
    fields = ['grade', 'title', 'image', 'hint_approach', 'hint_approach_image', 'hint_formula', 'hint_formula_image', 'hint_technique', 'hint_technique_image', 'tags']
    template_name = 'math_app/problem_form.html'
    success_url = reverse_lazy('problem_list')
    login_url = 'login'
    
    def get_context_data(self, **kwargs):
        """
        テンプレートに学年と単元の情報を追加
        """
        context = super().get_context_data(**kwargs)
        context['grades'] = Grade.objects.all().order_by('order')
        
        # 選択された学年がある場合、その学年の単元を追加
        if self.request.GET.get('grade'):
            try:
                selected_grade = Grade.objects.get(id=self.request.GET.get('grade'))
                context['selected_grade'] = selected_grade
                context['tags_for_grade'] = Tag.objects.filter(grade=selected_grade).order_by('name')
            except Grade.DoesNotExist:
                pass
        
        return context
    
    def form_valid(self, form):
        """フォーム送信時、ログインユーザーを自動で割り当て"""
        form.instance.user = self.request.user
        messages.success(self.request, '問題を登録しました')
        return super().form_valid(form)


# ==============================================================================
# 2) 問題詳細ビュー（DetailView + ヒント編集機能）
# ==============================================================================
class ProblemDetailView(LoginRequiredMixin, DetailView):
    """
    問題の詳細を表示し、ヒント（方針・公式・コツ）を表示・編集するビュー
    """
    model = Problem
    template_name = 'math_app/problem_detail.html'
    context_object_name = 'problem'
    login_url = 'login'
    
    def get_queryset(self):
        """ログインユーザーの問題のみ取得"""
        return Problem.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """テンプレートにヒント情報を追加"""
        context = super().get_context_data(**kwargs)
        problem = self.get_object()
        
        # ヒント情報を取得
        context['hint_approach'] = problem.hint_approach
        context['hint_formula'] = problem.hint_formula
        context['hint_technique'] = problem.hint_technique
        context['tags'] = problem.tags.all()
        
        return context


# 問題更新（UpdateView）
class ProblemUpdateView(LoginRequiredMixin, UpdateView):
    model = Problem
    fields = ['grade', 'title', 'hint_approach', 'hint_approach_image', 'hint_formula', 'hint_formula_image', 'hint_technique', 'hint_technique_image', 'tags']
    template_name = 'math_app/problem_form.html'
    login_url = 'login'
    
    def get_queryset(self):
        return Problem.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = Grade.objects.all().order_by('order')
        
        # 現在の問題の学年に該当する単元を取得
        problem = self.get_object()
        if problem.grade:
            context['selected_grade'] = problem.grade
            context['tags_for_grade'] = Tag.objects.filter(grade=problem.grade).order_by('name')
        
        return context
    
    def get_success_url(self):
        return reverse_lazy('problem_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, '問題を更新しました')
        return super().form_valid(form)


# 問題削除（DeleteView）
class ProblemDeleteView(LoginRequiredMixin, DeleteView):
    model = Problem
    template_name = 'math_app/problem_confirm_delete.html'
    success_url = reverse_lazy('problem_list')
    login_url = 'login'
    
    def get_queryset(self):
        return Problem.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '問題を削除しました')
        return super().delete(request, *args, **kwargs)


# 問題一覧（ListView：検索・フィルタ機能あり）
class ProblemListView(LoginRequiredMixin, ListView):
    model = Problem
    template_name = 'math_app/problem_list.html'
    context_object_name = 'problems'
    paginate_by = 12
    login_url = 'login'
    
    def get_queryset(self):
        queryset = Problem.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
        
        # タグフィルタ
        tag_id = self.request.GET.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)
        
        # 検索フィルタ
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(hint_approach__icontains=search_query) |
                Q(hint_formula__icontains=search_query) |
                Q(hint_technique__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # ユーザーが使用しているすべてのタグを取得
        user_tags = Tag.objects.filter(
            problems__user=self.request.user
        ).distinct()
        
        context['tags'] = user_tags
        context['selected_tag'] = self.request.GET.get('tag')
        context['search_query'] = self.request.GET.get('q')
        
        return context


# タグ別アーカイブ
class TagArchiveView(LoginRequiredMixin, ListView):
    model = Problem
    template_name = 'math_app/tag_archive.html'
    context_object_name = 'problems'
    paginate_by = 12
    login_url = 'login'
    
    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, id=tag_id)
        
        return Problem.objects.filter(
            user=self.request.user,
            tags=tag
        ).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        context['tag'] = get_object_or_404(Tag, id=tag_id)
        return context


# 認証ビュー
def login_view(request):
    if request.user.is_authenticated:
        return redirect('problem_list')
    
    next_url = request.GET.get('next') or request.POST.get('next')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'ログインしました')
            return redirect(next_url or 'problem_list')
        else:
            messages.error(request, 'ユーザー名またはパスワードが正しくありません')
    else:
        form = AuthenticationForm(request)
    
    return render(request, 'math_app/auth_login.html', {'form': form, 'next': next_url})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'ログアウトしました')
    return redirect('index')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('problem_list')
    
    next_url = request.GET.get('next') or request.POST.get('next')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'アカウントを作成してログインしました')
            return redirect(next_url or 'problem_list')
        else:
            messages.error(request, '入力内容を確認してください')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'math_app/auth_signup.html', {
        'form': form,
        'next': next_url
    })


# AJAX: 学年に紐づく単元タグ取得
@login_required(login_url='login')
@require_http_methods(["GET"])
def tags_by_grade(request, grade_id):
    tags = Tag.objects.filter(grade_id=grade_id).order_by('subject', 'order', 'name')
    data = {
        'tags': [{'id': tag.id, 'name': tag.name} for tag in tags]
    }
    return JsonResponse(data)


# AJAX: 科目に紐づく単元タグ取得
@login_required(login_url='login')
@require_http_methods(["GET"])
def tags_by_subject(request, subject_id):
    tags = Tag.objects.filter(subject_id=subject_id).order_by('order', 'name')
    data = {
        'tags': [{'id': tag.id, 'name': tag.name} for tag in tags]
    }
    return JsonResponse(data)


# AJAX: 学年に紐づく科目取得
@login_required(login_url='login')
@require_http_methods(["GET"])
def subjects_by_grade(request, grade_id):
    subjects = Subject.objects.filter(grade_id=grade_id).order_by('order', 'name')
    data = {
        'subjects': [{'id': subject.id, 'name': subject.name} for subject in subjects]
    }
    return JsonResponse(data)


# AJAX: ヒント更新
@login_required(login_url='login')
@require_http_methods(["POST"])
def update_hint(request, pk):
    try:
        import json
        
        # 問題を取得
        problem = get_object_or_404(Problem, id=pk, user=request.user)
        
        # リクエストをパース
        data = json.loads(request.body)
        hint_type = data.get('hint_type', '').strip()
        content = data.get('content', '').strip()
        
        # バリデーション
        if not hint_type or hint_type not in ['approach', 'formula', 'technique']:
            return JsonResponse({
                'success': False,
                'message': '不正なヒント種類です'
            }, status=400)
        
        # ヒントを更新
        if hint_type == 'approach':
            problem.hint_approach = content
        elif hint_type == 'formula':
            problem.hint_formula = content
        elif hint_type == 'technique':
            problem.hint_technique = content
        
        problem.save()
        
        logger.info(f"ヒント更新: Problem={pk}, type={hint_type}")
        
        return JsonResponse({
            'success': True,
            'message': 'ヒントを保存しました'
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'リクエスト形式が不正です'
        }, status=400)
    
    except Exception as e:
        logger.error(f"ヒント更新エラー: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': f'エラーが発生しました: {str(e)}'
        }, status=500)


# 質問フォームビュー
def question_view(request):
    """開発者への質問フォーム"""
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        
        if form.is_valid():
            question = form.save(commit=False)
            
            # ログインユーザーがいれば紐付ける
            if request.user.is_authenticated:
                question.user = request.user
            
            question.save()
            
            # メール送信
            from django.core.mail import send_mail
            from django.conf import settings
            
            try:
                # 管理者へのメール
                admin_message = f"""
新しい質問が届きました。

【質問者情報】
お名前: {question.name}
メールアドレス: {question.email}
ユーザー: {question.user.username if question.user else '未登録'}

【質問内容】
件名: {question.subject}

{question.message}

---
送信日時: {question.created_at.strftime('%Y年%m月%d日 %H:%M')}
"""
                
                send_mail(
                    subject=f'【MathHint】新しい質問: {question.subject}',
                    message=admin_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['ksw2570215@stu.o-hara.ac.jp'],
                    fail_silently=False,
                )
                
                messages.success(request, '質問を送信しました。返信までお待ちください。')
            except Exception as e:
                logger.error(f'メール送信エラー: {str(e)}')
                messages.warning(request, '質問は保存されましたが、メール送信に失敗しました。直接メールでお問い合わせください。')
            
            return redirect('question_success')
        else:
            messages.error(request, '入力内容を確認してください。')
    else:
        form = QuestionForm()
        
        # ログインユーザーの情報を自動入力
        if request.user.is_authenticated:
            form.initial['name'] = request.user.username
            form.initial['email'] = request.user.email
    
    return render(request, 'math_app/question_form.html', {'form': form})


def question_success(request):
    """質問送信完了ページ"""
    return render(request, 'math_app/question_success.html')

