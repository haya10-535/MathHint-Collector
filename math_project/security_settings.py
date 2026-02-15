# セキュリティ関連の設定ファイル

# ============================================
# 1. パスワードポリシー強化
# ============================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # 最低 8 文字
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # カスタム validator: 複雑性チェック
    'math_app.validators.ComplexPasswordValidator',
]

# ============================================
# 2. セッション設定強化
# ============================================
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # データベース保存
SESSION_COOKIE_SECURE = True  # HTTPS のみ
SESSION_COOKIE_HTTPONLY = True  # JavaScript からアクセス不可
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF 対策
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # ブラウザ閉じたらセッション削除
SESSION_COOKIE_AGE = 3600  # 1 時間でタイムアウト
SESSION_SAVE_EVERY_REQUEST = True  # リクエストごとに更新

# ============================================
# 3. CSRF 設定強化
# ============================================
CSRF_COOKIE_SECURE = True  # HTTPS のみ
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_TRUSTED_ORIGINS = [
    # 環境に応じて許可するドメインを追加
]

# ============================================
# 4. セキュリティミドルウェア設定
# ============================================
SECURE_BROWSER_XSS_FILTER = True  # XSS フィルタ
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'"),  # 必要に応じて調整
    'style-src': ("'self'", "'unsafe-inline'"),
    'img-src': ("'self'", "data:", "https:"),
}

# ============================================
# 5. HTTPS 強制
# ============================================
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 年間
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ============================================
# 6. django-axes レート制限設定
# ============================================
AXES_FAILURE_LIMIT = 5  # 5 回失敗でロック
AXES_COOLOFF_DURATION = 30  # 30 分間ロック
AXES_LOCK_OUT_AT_FAILURE = True
AXES_USE_USER_AGENT = True
AXES_LOCK_OUT_TEMPLATE = 'math_app/lockout.html'  # ロック画面テンプレート
AXES_VERBOSE = True  # ログ詳細
