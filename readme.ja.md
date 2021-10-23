# 日本語説明

Python3で開発したCloudFlare DDNSスクリプト。

## 要件

Linuxシステム（Windows不可）

python >=3.6

## 使用方法

### 1.python3.6以降のバージョンをインスト

略

### 2.下記の通りに実行

```bash
pip3 install requests dnspython func-timeout
git clone https://github.com/LDLDL/cfddns.git
```
### 3.install_as_service.shを実行してから配置します

`sudo bash install_as_service.sh`

## 配置

配置に先立って、配置したいドメイン名を配置しておきます。

例えばddns.example.comは配置したい場合は、まずCloudFlareのコントロールパネルでAレコードまたAAAAレコードに追加。そのIPアドレスは自分が使っているIPと同じではいけない。（同じにすればいいですが、すぐに動作するかどうかはわかりにくいですから）

install_as_service.shを実行すると、配置メニューに入ります。

![g00](https://user-images.githubusercontent.com/81149482/129917531-d499ae47-79ab-44b0-910b-e1f2a98fc68c.png)

Email: CloudFlareで登録したメールアドレスです。

Zones: 対応のドメイン名のOverviewページで、右下にあったZone ID

API Key: [ここ](https://dash.cloudflare.com/profile/api-tokens)をクリック、Global API Keyの右にviewをクリックすると、表示された英数字がAPI Keyです。

配置が完成してから3を入力してドメイン名を追加する。

Domain: 配置したいドメイン名。例えばddns.example.com

domain record type(A for v4, AAAA for v6)：レコードの種類。AはAレコード、AAAAはAAAAレコードです。

全部が完了した後で、もしエラー情報が返したら、もう一度API Tokenなど配置したものをしっかり確認するのが必要だと思います。

## ドメイン名の追加

もしすでに配置しましたスクリプトに新しいドメイン名を追加したい場合は、下記の通りに従います。

1.このプロジェクトのフォルダに入る。例えばcfddns
2.`sudo python3 ./config.py`を実行
3.3を押して、最初と同じドメイン名を追加する。
4.サービスを起動する。`systemctl cfddns restart`

## エラーに対して問題

install_as_service.shを実行する際にインストできない場合は、ご使用中のシステムのsystemdフォルダを探して、それからcfddns.serviceをそれに入っておきます。

もしエラーがpython3が見つかりませんったら、その場合はcfddns.serviceでpython3の絶対パスに書き換えます。（ここで相対パスに入力すればたまに動作可能ですが、交換性を保つため絶対パスに入力するのがお勧めです。）
