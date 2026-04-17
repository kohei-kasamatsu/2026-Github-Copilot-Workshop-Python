# API リファレンス

## 概要

現時点では REST API エンドポイントは実装されていない。Flask アプリケーションはトップページの HTML 配信のみを行い、タイマー設定はサーバーサイドレンダリングによってページに埋め込まれる。

---

## 画面エンドポイント

### GET /

ポモドーロタイマーのトップページを返す。

**レスポンス**

- ステータスコード: `200 OK`
- Content-Type: `text/html`

**テンプレート変数**

| 変数名 | 型 | 説明 |
|---|---|---|
| `page_title` | `str` | ページタイトル（例: `"Pomodoro Timer"`） |
| `initial_settings` | `dict` | タイマー初期設定（JSON として埋め込まれる） |

**`initial_settings` のフィールド**

| フィールド名 | 型 | デフォルト値 | 説明 |
|---|---|---|---|
| `workDurationMinutes` | `int` | `25` | 作業セッションの長さ（分） |
| `shortBreakMinutes` | `int` | `5` | 短休憩の長さ（分） |
| `longBreakMinutes` | `int` | `15` | 長休憩の長さ（分） |
| `longBreakInterval` | `int` | `4` | 長休憩に入るまでの作業セッション回数 |

**HTML への埋め込み形式**

初期設定は `id="initial-settings"` を持つ `<script type="application/json">` タグに JSON 形式で埋め込まれる。

```html
<script id="initial-settings" type="application/json">
{"workDurationMinutes": 25, "shortBreakMinutes": 5, "longBreakMinutes": 15, "longBreakInterval": 4}
</script>
```

---

## 将来的な API 拡張候補

以下のエンドポイントは現時点では未実装だが、将来の拡張として想定されている。

| メソッド | パス | 説明 |
|---|---|---|
| `GET` | `/api/settings` | タイマー設定の取得 |
| `GET` | `/api/stats/today` | 今日の進捗統計の取得 |
| `POST` | `/api/sessions` | 完了セッションの保存 |
