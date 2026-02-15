from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # 問題CRUD
    path('problems/', views.ProblemListView.as_view(), name='problem_list'),
    path('problem/new/', views.ProblemCreateView.as_view(), name='problem_new'),
    path('problem/<int:pk>/', views.ProblemDetailView.as_view(), name='problem_detail'),
    path('problem/<int:pk>/edit/', views.ProblemUpdateView.as_view(), name='problem_edit'),
    path('problem/<int:pk>/delete/', views.ProblemDeleteView.as_view(), name='problem_delete'),

    # タグ別アーカイブ
    path('tag/<int:tag_id>/', views.TagArchiveView.as_view(), name='tag_archive'),

    # ヒント更新API
    path('problem/<int:pk>/hint/update/', views.update_hint, name='update_hint'),

    # 学年・科目・単元API
    path('api/grades/<int:grade_id>/tags/', views.tags_by_grade, name='tags_by_grade'),
    path('api/subjects/<int:subject_id>/tags/', views.tags_by_subject, name='tags_by_subject'),
    path('api/grades/<int:grade_id>/subjects/', views.subjects_by_grade, name='subjects_by_grade'),

    # 認証
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    
    # 質問フォーム
    path('question/', views.question_view, name='question'),
    path('question/success/', views.question_success, name='question_success'),
]
