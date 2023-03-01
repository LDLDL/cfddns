# 日本語説明

Python3で開発したCloudFlare DDNSスクリプト。

## 要件

python >=3.6

## 使用方法

### 1.python3.6以降のバージョンをインスト

略

### 2.下記の通りに実行

```bash
git clone https://github.com/LDLDL/cfddns.git
cd cfddns
pip3 install -r requirements.txt
```
### 3.実行

### 実行パラメータ

- [--conf] ファイルパス。ロードされる配置ファイルのパスを指定する。デフォルトは現在のフォルダーのconf.jsonです。
- [--log] ファイルパス，ログファイルの保存パスを指定します。
- [--onetime] IPアドレスが一回通知完了後終了します。Crontab向けパラメータです。
- [--usedns] 現在のドメインIPアドレスを取得時にCloudFlare APIで確認しない。DNSで名称解決を行います。
- [--nolog] ログを記録しません。コンソールだけに出力します。

#### Linux

下記のコマンドを実行

`sudo bash install_systemd_service.sh`

これで自動的に設定ガイドに入り、配置が完了した後で自動的にシステムサービスとしてインストールされています。

#### 共通システム

##### 手動で実行

1. ターミナルで本プロジェクトのフォルダに入り、`python3 config.py`を実行して必要情報を登録しておきます。  
2. `python3 cfddns.py`を実行

##### スケジュールタスク

1. ターミナルで本プロジェクトのフォルダに入り、`python3 config.py`を実行して必要情報を登録しておきます。  
2. スケジュールタスクで下記のコマンドを添えます。

`python3 {path to cfddns.py} --onetime --conf {path to conf.json}`

括弧内のpath to cfddns.pyは実際の絶対パスに替えてください。
Onetimeモードでデフォルトログはファイルに保存していない。--log ファイル名のパラメータでログファイルの出力を指定できます。

#### Windowsの自動起動設定方法

1. このプロジェクトのinstall_systemd_serviceフォルダ内のddns.vbs,run.batをcfddns.pyと同じフォルダにコピーします。それからddns.vbs, run,batのパスを実際のパスに変更します。例えはC:\cfddns
2. cfddns.reg内のパスも編集します。wscript.exeの後はスクリプトパス。wscript.exeを変更しないでください。
3. ダブルクリックcfddns.reg、それを有効にします。

## 配置

配置に先立って、配置したいドメイン名を配置しておきます。

例えばddns.example.comは配置したい場合は、まずCloudFlareのコントロールパネルでAレコードまたAAAAレコードに追加。そのIPアドレスは自分が使っているIPと同じではいけない。（同じにすればいいですが、すぐに動作するかどうかはわかりにくいですから）

install_systemd_service.shを実行すると、配置メニューに入ります。

![g00](https://user-images.githubusercontent.com/81149482/129917531-d499ae47-79ab-44b0-910b-e1f2a98fc68c.png)

Email: CloudFlareで登録したメールアドレスです。

Zones: 対応のドメイン名のOverviewページで、右下にあったZone ID

API Key: [ここ](https://dash.cloudflare.com/profile/api-tokens)をクリック、Global API Keyの右にviewをクリックすると、表示された英数字がAPI Keyです。

配置が完成してから3を入力してドメイン名を追加する。

Domain: 配置したいドメイン名。例えばddns.example.com

domain record type(A for v4, AAAA for v6)：レコードの種類。AはAレコード、AAAAはAAAAレコードです。

全部が完了した後、もしエラー情報が返したら、もう一度API Tokenなど配置したものをしっかり確認するのが必要だと思います。

## ドメイン名の追加

もしすでに配置しましたスクリプトに新しいドメイン名を追加したい場合は、下記の通りに従います。

### Linux

1. このプロジェクトのフォルダに入る。例えばcfddns
2. `sudo python3 ./config.py`を実行
3. 3を押して、最初と同じドメイン名を追加する。
4. サービスを起動する。`systemctl restart cfddns`


### 共通システム

1. cfddns.pyを終止する
2. config.pyを実行して新しいドメイン情報を入力する
3. 設定ガイドが完了した後でcfddns.pyを実行する

## エラーに対して問題

install_systemd_service.shを実行する際にインストできない場合は、ご使用中のシステムのsystemdフォルダを探して、それからcfddns.serviceをそれに入っておきます。

もしエラーがpython3が見つかりませんったら、その場合は（もしWindowsの場合はPythonを書き換える）cfddns.serviceでpython3の絶対パスに書き換えます。（ここで相対パスに入力すればたまに動作可能ですが、交換性を保つため絶対パスに入力するのがお勧めです。）
