# アーキテクチャ概要

## 1. 全体方針

Flask をページ配信に使用し、タイマーの状態管理とカウントダウンはブラウザ側で実行する構成を採用している。タイマー処理はサーバーに依存せず、ブラウザ上で完結する。

---

## 2. レイヤー構成

```
1.pomodoro/
├── app.py                      # Flask アプリケーションエントリポイント
├── config.py                   # アプリケーション設定
├── services/
│   └── pomodoro_service.py     # サービス層（業務ロジック）
├── templates/
│   └── index.html              # HTML テンプレート
├── static/
│   ├── css/
│   │   └── style.css           # スタイルシート
│   └── js/
│       ├── timer-ui.js         # フロントエンドエントリポイント
│       ├── timer-store.js      # 状態管理
│       ├── timer-core.js       # タイマーコアロジック
│       └── storage.js          # localStorage アダプタ
└── tests/
    ├── test_app.py             # Flask テスト
    └── test_pomodoro_service.py # サービステスト
```

---

## 3. 各レイヤーの責務

### 3.1 Flask 層（`app.py`）

- `create_app()` ファクトリ関数で Flask アプリケーションを生成する
- `AppConfig` から設定を読み込む
- `GET /` ルートでトップページを配信する
- `get_initial_settings()` で取得した初期設定をテンプレートに渡す

### 3.2 設定層（`config.py`）

- `AppConfig` クラスにタイマー設定を集約する
- 設定値はクラス変数として定義される（環境変数や外部ファイルは使用しない）

### 3.3 サービス層（`services/pomodoro_service.py`）

- Flask のルート処理から業務ロジックを分離する
- `get_initial_settings(config)` が Flask 設定辞書を受け取り、フロントエンド向けのキー名に変換して返す

### 3.4 テンプレート層（`templates/index.html`）

- タイマー画面の HTML 構造を定義する
- Flask から受け取った `initial_settings` を `<script type="application/json">` タグに JSON として埋め込む
- `timer-ui.js` をモジュールとして読み込む

### 3.5 フロントエンド層（`static/js/`）

フロントエンドは 4 つのモジュールで構成される。

| ファイル | 役割 |
|---|---|
| `storage.js` | localStorage からの初期設定読み込み |
| `timer-core.js` | タイマー状態の初期値生成（pure function） |
| `timer-store.js` | 状態管理ストア（`timer-core.js` を利用） |
| `timer-ui.js` | エントリポイント（`storage.js`, `timer-store.js` を呼び出す） |

---

## 4. データフロー

```
[config.py]
    ↓ AppConfig
[app.py: create_app()]
    ↓ app.config
[services/pomodoro_service.py: get_initial_settings()]
    ↓ initial_settings dict
[templates/index.html]
    ↓ <script id="initial-settings" type="application/json">
[static/js/storage.js: loadInitialSettings()]
    ↓ settings object
[static/js/timer-store.js: createTimerStore()]
    ↓ store
[window.pomodoroApp]
```

---

## 5. 現在の実装状態

MVP の初期段階として、以下が実装済みである。

- Flask によるトップページ配信
- タイマー設定のサーバーサイド注入とフロントエンドでの読み込み
- タイマー初期状態の生成（作業モード、指定分数）
- HTML/CSS による画面の骨組み（静的表示）

以下は設計上想定されているが、現時点では未実装である。

- タイマーのカウントダウン・開始・停止・リセット操作
- モード遷移（作業 → 休憩 → 作業）
- localStorage を使った状態保存と復元
- 今日の進捗表示
