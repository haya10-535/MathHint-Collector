# JSON の基本

## JSONの 6つのデータ型

| 型 | 例 | 説明 |
|:---|:---|:---|
| **文字列** | `"hello"` | ダブルクォートで囲む |
| **数値** | `123`, `3.14` | 整数または小数 |
| **ブール値** | `true`, `false` | 真偽値（小文字） |
| **null** | `null` | 空の値 |
| **配列** | `[1, "a"]` | `[]` で囲んだリスト |
| **オブジェクト** | `{"key": "value"}` | `{}` で囲んだ構造体 |

## JSONオブジェクトの基本ルール

```json
{
  "name": "Alice",
  "age": 30,
  "email": "alice@example.com",
  "is_active": true,
  "score": null,
  "skills": ["Python", "JavaScript", "SQL"],
  "address": {
    "city": "Tokyo",
    "zip": "100-0001"
  }
}
```

### ルール
- ✓ **キーは必ず文字列** → `"key"` でダブルクォートで囲む
- ✓ **値はいろいろ型OK** → 文字列、数値、真偽値、null、配列、オブジェクト
- ✓ **ブール値は小文字** → `true`, `false` （`True`, `False` NG）
- ✓ **null は小文字** → `null` （`None`, `undefined` NG）
- ✗ **コメント不可** → `//` や `/* */` は使えない
- ✗ **末尾のカンマなし** → `[1, 2,]` はエラー

## よくあるエラー

❌ **シングルクォート**
```json
{'name': 'Alice'}  // エラー！ダブルクォートが必須
```

✓ **正しい**
```json
{"name": "Alice"}
```

---

❌ **Python の True/False/None**
```json
{"is_active": True, "data": None}  // エラー！
```

✓ **正しい**
```json
{"is_active": true, "data": null}
```

---

❌ **コメント**
```json
{
  "name": "Alice"  // こんにちは ← エラー！
}
```

✓ **正しい**
```json
{
  "name": "Alice"
}
```

---

❌ **末尾のカンマ**
```json
{
  "name": "Alice",
  "age": 30,  // ← このカンマはエラー
}
```

✓ **正しい**
```json
{
  "name": "Alice",
  "age": 30
}
```

## JSON ファイルの読み込み・保存

```python
import json

# JSONファイルを読む
with open('math_seed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# JSONファイルに保存
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

## JSON の用途

- 📡 **API通信** - サーバー間のデータ交換
- 💾 **設定ファイル** - アプリの設定保存（`package.json` など）
- 📦 **データベース** - NoSQL（MongoDB など）のデータ形式
- 🎯 **その他** - 言語を問わず使える標準フォーマット
