# データモデル仕様

## 1. サーバーサイドデータモデル

### 1.1 AppConfig（設定クラス）

**ファイル**: `config.py`

Flask アプリケーション設定を保持するクラス。インスタンス化せずにクラス変数として使用する。

| フィールド名 | 型 | 値 | 説明 |
|---|---|---|---|
| `APP_TITLE` | `str` | `"Pomodoro Timer"` | アプリケーションタイトル |
| `WORK_DURATION_MINUTES` | `int` | `25` | 作業セッション時間（分） |
| `SHORT_BREAK_MINUTES` | `int` | `5` | 短休憩時間（分） |
| `LONG_BREAK_MINUTES` | `int` | `15` | 長休憩時間（分） |
| `LONG_BREAK_INTERVAL` | `int` | `4` | 長休憩に入るまでの作業セッション回数 |

---

### 1.2 initial_settings（サービス出力）

**生成元**: `services/pomodoro_service.py` の `get_initial_settings(config)`

`AppConfig` の設定値をフロントエンド向けのキー名（camelCase）に変換した辞書。HTML テンプレートに JSON として埋め込まれる。

| フィールド名 | 型 | 対応する AppConfig フィールド | 説明 |
|---|---|---|---|
| `workDurationMinutes` | `int` | `WORK_DURATION_MINUTES` | 作業セッション時間（分） |
| `shortBreakMinutes` | `int` | `SHORT_BREAK_MINUTES` | 短休憩時間（分） |
| `longBreakMinutes` | `int` | `LONG_BREAK_MINUTES` | 長休憩時間（分） |
| `longBreakInterval` | `int` | `LONG_BREAK_INTERVAL` | 長休憩に入るまでの回数 |

**例**:

```json
{
  "workDurationMinutes": 25,
  "shortBreakMinutes": 5,
  "longBreakMinutes": 15,
  "longBreakInterval": 4
}
```

**エラー挙動**: `config` 辞書に必須キーが存在しない場合、`KeyError` を送出する。

---

## 2. フロントエンドデータモデル

### 2.1 settings（読み込み済み設定）

**生成元**: `storage.js` の `loadInitialSettings()`

HTML の `id="initial-settings"` 要素から読み込んだ設定オブジェクト。`initial_settings` と同一の構造を持つ。

| フィールド名 | 型 | 説明 |
|---|---|---|
| `workDurationMinutes` | `number` | 作業セッション時間（分） |
| `shortBreakMinutes` | `number` | 短休憩時間（分） |
| `longBreakMinutes` | `number` | 長休憩時間（分） |
| `longBreakInterval` | `number` | 長休憩に入るまでの回数 |

要素が存在しない場合は `null` を返す。

---

### 2.2 timerState（タイマー状態）

**生成元**: `timer-core.js` の `createInitialTimerState(settings)`

タイマーの初期状態を表すオブジェクト。

| フィールド名 | 型 | 初期値 | 説明 |
|---|---|---|---|
| `mode` | `string` | `"work"` | 現在のタイマーモード |
| `durationMinutes` | `number` | `settings.workDurationMinutes` | 現在モードの合計時間（分） |

**`mode` の取りうる値（設計上）**:

| 値 | 説明 |
|---|---|
| `"work"` | 作業セッション |
| `"short_break"` | 短休憩（未実装） |
| `"long_break"` | 長休憩（未実装） |

---

### 2.3 store（状態ストア）

**生成元**: `timer-store.js` の `createTimerStore(settings)`

タイマー状態へのアクセスを提供するオブジェクト。

| メソッド | 引数 | 戻り値 | 説明 |
|---|---|---|---|
| `getState()` | なし | `timerState` | 現在のタイマー状態を返す |

---

### 2.4 window.pomodoroApp（グローバル公開オブジェクト）

**生成元**: `timer-ui.js`

ブラウザの `window` オブジェクトに公開されるアプリケーション状態。`settings` が取得できた場合にのみ設定される。

| フィールド名 | 型 | 説明 |
|---|---|---|
| `settings` | `object` | 読み込んだタイマー設定 |
| `store` | `object` | タイマー状態ストア |
