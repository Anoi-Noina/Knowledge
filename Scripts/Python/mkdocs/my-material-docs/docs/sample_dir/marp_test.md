---
marp: true
theme: default
size: 16:9
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1em;
  }
---

# Marp スライドのテスト

### MkDocsへの埋め込みテスト用

---
# 基本的な構造

- Markdownのリスト形式で簡単に箇条書きが作れます。
- MarpはMarkdownを自動でスライドに変換します。

---

# 機能の紹介 (カスタマイズ)

## 2カラムレイアウトの例

<div class="columns">
  <div>
    ### 左側 (コンテンツ)
    - **Markdown** で書けます。
    - **コードブロック** も対応。
    
    ```python
    def hello_mkdocs():
        print("Hello, MkDocs!")
    ```
  </div>

  <div>
    ### 右側 (画像)
    ![bg vertical fit](https://placehold.jp/250x250.png)
  </div>
</div>

---

# ページ番号と背景

## このスライドは 3 ページ目です

* 自動でページ番号が表示されます。
* 背景色や背景画像を簡単に設定できます。

---

# アニメーション効果

### 要素を段階的に表示 (Fragments)

- これは最初に表示されます。
- - [TOC]
- これが最後の行です。