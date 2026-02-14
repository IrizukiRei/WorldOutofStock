# WorldOutofStock

`RULEBOOK.md` のルールを実際に遊べる実装です。CLI版に加えて、ブラウザ版も追加しました。

## CLI版

```bash
python3 game.py
```

## ブラウザ版

```bash
python3 web_server.py
# then open http://localhost:8000/web/index.html
```

## 実装範囲

- 第一部：消滅ゲーム（必要5項目の入力と消滅宣言）
- 世襲：国家欠損→空札色
- 第二部：5ターン基本ゲーム（内政3ターン＋外交2ターン）
- 事件コイントス（ターン4のみねじれ判定）
- 同色共鳴による世界在庫加点、空札無効、最終エンド判定

> 拡張カセット（発火/贔屓/神話/生存）は、現時点では未実装です。


## トラブルシュート

- ブラウザで何も表示されない場合は、`python3 web_server.py` を起動したまま `http://localhost:8000/web/index.html` を開いてください。
- `localhost` で繋がらない環境では `http://127.0.0.1:8000/web/index.html` も試してください。
