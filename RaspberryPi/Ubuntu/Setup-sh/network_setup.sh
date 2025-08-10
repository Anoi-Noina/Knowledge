#!/bin/bash
set -e

CONFIG_FILE="/etc/netplan/99-custom.yaml"


# ファイルが存在する場合にバックアップ作成
if [ -f "$CONFIG_FILE" ]; then
    sudo cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
    echo "バックアップを作成しました: ${CONFIG_FILE}.bak"
else
    echo "元の設定ファイルが存在しません: $CONFIG_FILE"
fi

# 一時ファイルへ出力
TMP_FILE=$(mktemp)

echo "network:" > "$TMP_FILE"
echo "  version: 2" >> "$TMP_FILE"
echo "  ethernets:" >> "$TMP_FILE"

default_route_set=false

while true; do
    # インターフェース一覧を取得して選ばせる
    interfaces=($(ls /sys/class/net | grep -v lo))
    echo "使用するインターフェースを選んでください："
    select iface in "${interfaces[@]}" "終了"; do
        [[ "$REPLY" -gt 0 && "$REPLY" -le "${#interfaces[@]}" ]] && break
        [[ "$REPLY" -eq $((${#interfaces[@]}+1)) ]] && exit 0
        echo "無効な選択です"
    done

    # ローカルかどうかの選択
    while true; do
        read -p "このインターフェースはローカルですか？ (y/n): " is_local
        case "$is_local" in
            y|Y )
                read -p "固定IPアドレス (例: 192.168.1.100/24): " ipaddr
                echo "    $iface:" >> "$TMP_FILE"
                echo "      optional: true" >> "$TMP_FILE"
                echo "      dhcp4: false" >> "$TMP_FILE"
                echo "      dhcp6: false" >> "$TMP_FILE"
                echo "      addresses:" >> "$TMP_FILE"
                echo "        - $ipaddr" >> "$TMP_FILE"
                break
                ;;
            n|N )
                read -p "固定IPアドレス (例: 192.168.1.100/24): " ipaddr
                read -p "DNS（カンマ区切り、例: 8.8.8.8,1.1.1.1）: " dns

                echo "    $iface:" >> "$TMP_FILE"
                echo "      optional: true" >> "$TMP_FILE"
                echo "      dhcp4: false" >> "$TMP_FILE"
                echo "      dhcp6: false" >> "$TMP_FILE"
                echo "      addresses:" >> "$TMP_FILE"
                echo "        - $ipaddr" >> "$TMP_FILE"

                if ! $default_route_set; then
                    read -p "このNICにデフォルトゲートウェイを設定しますか？ (y/n): " set_gw
                    if [[ "$set_gw" =~ ^[yY]$ ]]; then
                        read -p "ゲートウェイ (例: 192.168.1.1): " gateway
                        echo "      routes:" >> "$TMP_FILE"
                        echo "        - to: 0.0.0.0/0" >> "$TMP_FILE"
                        echo "          via: $gateway" >> "$TMP_FILE"
                        default_route_set=true
                    fi
                fi

                # DNS
                dns_list=$(echo "$dns" | tr ',' '\n' | sed 's/^/          - /')
                echo "      nameservers:" >> "$TMP_FILE"
                echo "        addresses:" >> "$TMP_FILE"
                echo "$dns_list" >> "$TMP_FILE"
                break
                ;;
            * ) echo "y または n を入力してください";;
        esac
    done

    echo
    read -p "さらに別のインターフェースを設定しますか？ (y/n): " cont
    [[ "$cont" =~ ^[nN]$ ]] && break
done

# 上書き
sudo mv "$TMP_FILE" "$CONFIG_FILE"
sudo chmod 600 "$CONFIG_FILE"

echo "設定が完了しました。'sudo netplan apply' を実行して反映してください。"
