# ShareGratitude

ありがとうと感謝を広げよう！という目的で、感謝ブログサイトを作っています。
ユーザ登録・ログイン・ポスト投稿というapiまで実装しています。フロントエンドとインフラは開発段階です。
バックエンドの動作確認は以下を参考にしてください！

必要なライブラリなどののインストール(pyproject.tomlの位置で実行)

```
poetry install
```

backend/.env.sample を .envファイルにコピーして環境変数を設定

```
cp backend/.env.sample .env
```

apiの実行

```
make run-api
```


api動作確認は、postmanでの実行を想定しています

- ユーザ登録

    http method post

    ```
    http://127.0.0.1:8000/users/register
    ```

    body(json)

    ```
    {
        "user_name": "take123",
        "user_email": "take@gmail.com",
        "password": "take123"
    }
    ```

- ユーザログイン

    http method post

    ```
    http://127.0.0.1:8000/auth/login
    ```

    body (json)

    ```
    {
        "user_email": "take@gmail.com",
        "password": "take123"
    }
    ```

- ポスト作成

    http method post

    ```
    http://127.0.0.1:8000/posts/create
    ```

    body (json)

    ```
    {
        "content": "take's first post",
        "mind": "so happy",
        "user_name": "take123"
    }
    ```

- ポストupdate

    http method post

    ```
    http://127.0.0.1:8000/posts/update/1
    ```

    body (json)
    
    ```
    {
        "content": " game",
        "mind": "temporary too sad."
    }
    ```

- ポスト削除

    http method delete

    ```
    http://127.0.0.1:8000/posts/delete/1
    ```

- 全てのポスト表示

    http method get

    ```
    http://127.0.0.1:8000/posts/
    ```

- ユーザの意見投稿(slackに通知)

    http method post

    ```
    http://127.0.0.1:8000/message/opinion/
    ```

    body (json)

    ```
    {
        "user_email": "take@gmail.com",
        "tag": "opinion",
        "content": "UI is not useful, you should update in the future."
    }
    ```