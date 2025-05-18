#!/bin/bash
set -e

echo "openssh-server をインストール中..."
sudo apt update
sudo apt install -y openssh-server

CONFIG_FILE="/etc/ssh/sshd_config"

# バックアップ
if [ -f "$CONFIG_FILE" ]; then
    sudo cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    echo "設定ファイルをバックアップしました: ${CONFIG_FILE}.bak"
fi

# 設定変更: rootログイン禁止（パスワードログインは維持）
echo "sshd_config を設定中..."

# コメントアウトされてるかどうかに関係なく上書き
sudo sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' "$CONFIG_FILE"
sudo sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication yes/' "$CONFIG_FILE"

# SSH サービス再起動
echo "sshd を再起動中..."
sudo systemctl restart ssh
sudo systemctl enable ssh

echo "SSH の設定が完了しました。"
