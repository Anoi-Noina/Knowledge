# M4 Mac Python環境構築備忘録 (2026年版)

M4チップの性能を活かしつつ、OS標準の環境を汚さない「Homebrew + uv」による構成。

## 1. コマンドラインツールの準備
Apple純正の開発ツールをインストールします。
```bash
xcode-select --install
```

## 2. Homebrew のインストール
macOS用パッケージマネージャーを導入し、パスを通します。
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# パスを通す (M4 Mac用)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## 3. uv のインストール
Python管理ツール `uv` を導入します。
```bash
brew install uv
```

## 4. Python のインストールと設定
Python 3.13をインストールし、シェルを更新します。
```bash
# Python 3.13のインストール
uv python install 3.13

# インストールしたPythonへのパスを通す
uv python update-shell

# 設定を反映
source ~/.zshrc
```

## 5. M4最適化設定 (JIT有効化)
M4チップの計算速度を向上させるためのオプション設定です。
```bash
echo 'export PYTHON_JIT=1' >> ~/.zshrc
source ~/.zshrc
```

## 6. プロジェクトの作成と仮想環境 (venv)
`uv` はプロジェクトディレクトリごとに独立した環境を構築します。

### プロジェクトの初期化
```bash
mkdir my-project && cd my-project
uv init
```

### 仮想環境の構築と同期
```bash
# 仮想環境 (.venv) を作成し、依存関係を同期する
uv sync

# 仮想環境の有効化
source .venv/bin/activate
```

## 7. パッケージの操作
`uv` は `pyproject.toml` を中心にパッケージを管理します。

### パッケージの追加・削除
```bash
# パッケージの追加 (pyproject.toml に自動追記)
uv add numpy pandas

# 開発用パッケージとして追加
uv add --dev pytest

# パッケージの削除
uv remove numpy
```

### 環境の再現
```bash
# pyproject.toml / uv.lock から環境を再構築する
uv sync
```

## 8. スクリプトの実行
仮想環境を明示的に有効化（activate）しなくても、`uv run` で実行可能です。
```bash
# 適切な環境でPythonファイルを実行
uv run main.py

# ツールを直接実行
uv run ruff check .
```

## 9. 便利な設定
### シェル補完の有効化
```bash
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
source ~/.zshrc
```

### キャッシュの削除
ディスク容量を節約したい場合に使用します。
```bash
uv cache clean
```