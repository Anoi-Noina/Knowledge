#!/bin/bash
set -e

echo "パッケージリストの更新中..."
sudo apt update

echo "アップグレード実行中..."
sudo apt upgrade -y

echo "不要なパッケージを削除中..."
sudo apt autoremove -y

echo "不要パッケージ（LibreOfficeなど）を削除中..."
sudo apt purge -y libreoffice* thunderbird*

sudo apt autoremove -y

if [ -f /var/run/reboot-required ]; then
  echo "再起動が必要です。再起動しますか？ (y/n)"
  read -r answer
  if [[ "$answer" =~ ^[Yy]$ ]]; then
    echo "再起動します..."
    sudo reboot
  else
    echo "再起動をスキップしました。"
  fi
else
  echo "再起動は不要です。"
fi
