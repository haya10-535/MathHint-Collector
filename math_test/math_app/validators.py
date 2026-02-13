"""
Django カスタム認証バリデータ
パスワード強度チェック、複雑さ検証など
"""

import re
from django.contrib.auth.password_validation import BasePasswordValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexPasswordValidator(BasePasswordValidator):
    """
    パスワード複雑度バリデータ
    必須要件:
    - 大文字（A-Z）を最低 1 文字含む
    - 小文字（a-z）を最低 1 文字含む
    - 数字（0-9）を最低 1 文字含む
    - 特殊文字（!@#$%^&*）を最低 1 文字含む
    """

    def __init__(self):
        self.special_chars = r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]'

    def validate(self, password, user=None):
        """パスワード複雑度をチェック"""
        errors = []

        # 大文字チェック
        if not re.search(r'[A-Z]', password):
            errors.append(
                ValidationError(
                    _('パスワードには大文字（A-Z）を最低 1 文字含める必要があります'),
                    code='no_uppercase',
                )
            )

        # 小文字チェック
        if not re.search(r'[a-z]', password):
            errors.append(
                ValidationError(
                    _('パスワードには小文字（a-z）を最低 1 文字含める必要があります'),
                    code='no_lowercase',
                )
            )

        # 数字チェック
        if not re.search(r'\d', password):
            errors.append(
                ValidationError(
                    _('パスワードには数字（0-9）を最低 1 文字含める必要があります'),
                    code='no_digit',
                )
            )

        # 特殊文字チェック
        if not re.search(self.special_chars, password):
            errors.append(
                ValidationError(
                    _('パスワードには特殊文字（!@#$%^&* など）を最低 1 文字含める必要があります'),
                    code='no_special_char',
                )
            )

        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        """バリデータのヘルプテキスト（登録画面に表示）"""
        return _(
            'パスワードは以下の条件をすべて満たす必要があります: '
            '大文字・小文字・数字・特殊文字をそれぞれ最低 1 文字含める'
        )
