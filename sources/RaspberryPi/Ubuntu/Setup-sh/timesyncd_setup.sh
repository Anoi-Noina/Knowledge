#!/bin/bash
set -e

# バックアップ
CONFIG_FILE="/etc/systemd/timesyncd.conf"
if [ -f "$CONFIG_FILE" ]; then
    sudo cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    echo "既存の設定を ${CONFIG_FILE}.bak にバックアップしました。"
fi

# NTPサーバ入力（IPアドレスのカンマ区切りもOK）
read -p "使用するNTPサーバをIPアドレスで入力してください（例: 133.243.238.163,133.243.238.164）: " ntp_servers

# timesyncd.conf を生成
sudo tee "$CONFIG_FILE" > /dev/null <<EOF
[Time]
NTP=${ntp_servers}
FallbackNTP=133.243.238.164
EOF

# サービスを再起動して反映
sudo systemctl restart systemd-timesyncd

# 有効化（自動起動）
sudo systemctl enable systemd-timesyncd

# 確認表示
timedatectl status
