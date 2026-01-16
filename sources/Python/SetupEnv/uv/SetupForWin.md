# Windows Python環境構築備忘録 (2026年版)

Windows環境でOSを汚さず、高速な `uv` を中心に据えた現代的な構成。

## 1. uv のインストール
Windows標準のパッケージマネージャー `winget` または公式スクリプトを使用します。

### PowerShell で実行
```powershell
# wingetを使用する場合
winget install astral-sh.uv

# インストール後、パスを反映させるためターミナルを再起動してください
```

## 2. Python のインストール
`uv` を使って、管理しやすい形で Python 3.13 を導入します。
```powershell
# Python 3.13のインストール
uv python install 3.13
```

## 3. 最適化設定 (JIT有効化)
Python 3.13のJITコンパイラを有効にするための環境変数を設定します。
```powershell
# ユーザー環境変数に設定
[System.Environment]::SetEnvironmentVariable('PYTHON_JIT', '1', 'User')

# 反映のため、一度PowerShellを閉じて開き直してください
```

## 4. プロジェクトの作成と仮想環境 (venv)
Windowsでもプロジェクトごとの管理が推奨されます。

### プロジェクトの初期化
```powershell
mkdir my-project
cd my-project
uv init
```

### 仮想環境の構築と同期
```powershell
# 仮想環境 (.venv) を作成し、依存関係を同期
uv sync

# 仮想環境の有効化 (Windows PowerShell用)
.venv\Scripts\activate
```

## 5. パッケージの操作
```powershell
# パッケージの追加
uv add numpy pandas

# 開発用パッケージの追加
uv add --dev pytest

# パッケージの削除
uv remove numpy
```

## 6. スクリプトの実行
activate（有効化）しなくても実行できる `uv run` が便利です。
```powershell
# 実行
uv run main.py
```

## 7. 便利な設定
### シェル補完の有効化 (PowerShell)
```powershell
if (!(Test-Path -Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }
Add-Content -Path $PROFILE -Value '(& uv generate-shell-completion powershell) | Out-String | Invoke-Expression'
```

### キャッシュの確認・削除
```powershell
# キャッシュの場所を確認
uv cache dir

# キャッシュ削除
uv cache clean
```