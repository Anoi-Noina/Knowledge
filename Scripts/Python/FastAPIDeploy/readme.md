# podmanを使ったfastapiアプリのデプロイ

## 環境
- Rocky Linux 10

## 手順

### ファイアウォールに通信許可するポートを追加

```bash
# sudo firewall-cmd --add-port=8000/tcp --permanent
sudo firewall-cmd --add-port=30080/tcp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

### イメージビルドからアプリ起動まで

- ディレクトリ構成
```bash
fastapi-app/
├── main.py
├── requirements.txt
└── Dockerfile
```

```bash
$ pwd
/home/goten/containers/fastapi-app

# -tでイメージにタグ名をつける
podman build -t localhost/fastapi-app:latest .

# イメージが作成されたことを確認
podman images

# コンテナを起動
podman run -d -p 30080:8000 --name fastapi fastapi-app:latest

# マニフェストファイルの作成（pod内のコンテナとしてのマニフェストファイルになる）
podman generate kube fastapi > fastapi-app.yml

# コンテナ停止
podman stop fastapi

# コンテナ
podman rm fastapi
```
