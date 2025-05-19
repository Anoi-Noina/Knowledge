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

# SSH接続確認後、パスワード認証を無効化
echo "sshで接続確認をして下さい"
while true; do
    read -p "パスワード認証を無効化しますか?: " yn
    case "$yn" in
        [yY]* )
            echo "パスワード認証を無効にします..."

            # PasswordAuthentication no に変更
            if grep -qE '^#?\s*PasswordAuthentication' "$CONFIG_FILE"; then
                sudo sed -i 's/^#*\s*PasswordAuthentication.*/PasswordAuthentication no/' "$CONFIG_FILE"
            else
                echo "PasswordAuthentication no" | sudo tee -a "$CONFIG_FILE" > /dev/null
            fi

            sudo systemctl restart ssh
            echo "パスワード認証を無効にし、sshd を再起動しました。"
            break
            ;;
        [nN]* )
            echo "設定は変更されていません。スクリプトを終了します。"
            break
            ;;
        * ) echo "y または n を入力してください。" ;;
    esac
done

echo "SSH の設定が完了しました。"
