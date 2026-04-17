# フロントエンドモジュール仕様

## 概要

フロントエンドは 4 つの ES モジュールで構成される。各モジュールは明確な責務を持ち、相互依存を最小限に抑えた設計になっている。

```
timer-ui.js          ← エントリポイント
  ├── storage.js     ← 初期設定の読み込み
  └── timer-store.js ← 状態ストア
        └── timer-core.js ← タイマーコアロジック
```

---

## モジュール詳細

### storage.js

**パス**: `static/js/storage.js`

localStorage および DOM からのデータ読み込みを担うアダプタモジュール。

#### `loadInitialSettings()`

HTML に埋め込まれた初期設定を読み込んで返す。

- `id="initial-settings"` の `<script type="application/json">` 要素のテキストを JSON としてパースする
- 要素が存在しない場合は `null` を返す

**戻り値**: `settings` オブジェクト または `null`

```js
import { loadInitialSettings } from "./storage.js";

const settings = loadInitialSettings();
// => { workDurationMinutes: 25, shortBreakMinutes: 5, longBreakMinutes: 15, longBreakInterval: 4 }
// または null（要素が存在しない場合）
```

---

### timer-core.js

**パス**: `static/js/timer-core.js`

タイマーのコアロジックを提供する純粋関数モジュール。DOM・localStorage に依存しない。

#### `createInitialTimerState(settings)`

設定オブジェクトを受け取り、タイマー初期状態を生成して返す。

| 引数 | 型 | 説明 |
|---|---|---|
| `settings` | `object` | タイマー設定（`workDurationMinutes` 等を含む） |

**戻り値**:

```js
{
  mode: "work",
  durationMinutes: settings.workDurationMinutes
}
```

```js
import { createInitialTimerState } from "./timer-core.js";

const state = createInitialTimerState({ workDurationMinutes: 25, ... });
// => { mode: "work", durationMinutes: 25 }
```

---

### timer-store.js

**パス**: `static/js/timer-store.js`

タイマー状態を保持・管理するストアモジュール。`timer-core.js` を利用する。

#### `createTimerStore(settings)`

設定を受け取り、状態ストアオブジェクトを生成して返す。

| 引数 | 型 | 説明 |
|---|---|---|
| `settings` | `object` | タイマー設定 |

**戻り値**: ストアオブジェクト

| メソッド | 説明 |
|---|---|
| `getState()` | `createInitialTimerState(settings)` を呼び出し、現在のタイマー状態を返す |

```js
import { createTimerStore } from "./timer-store.js";

const store = createTimerStore({ workDurationMinutes: 25, ... });
const state = store.getState();
// => { mode: "work", durationMinutes: 25 }
```

---

### timer-ui.js

**パス**: `static/js/timer-ui.js`

フロントエンドのエントリポイント。`storage.js` と `timer-store.js` を呼び出してアプリケーションを初期化する。

**処理フロー**:

1. `loadInitialSettings()` で設定を読み込む
2. 設定が取得できた場合、`createTimerStore(settings)` でストアを生成する
3. `window.pomodoroApp` に `settings` と `store` を公開する
4. 設定が取得できなかった場合（`null`）は何もしない

```js
// window.pomodoroApp の構造
window.pomodoroApp = {
  settings: { workDurationMinutes: 25, ... },
  store: {
    getState() { ... }
  }
};
```

**HTML から読み込む方法**:

```html
<script type="module" src="/static/js/timer-ui.js"></script>
```

---

## スタイルシート

### style.css

**パス**: `static/css/style.css`

アプリケーション全体のスタイルを定義する。

**主なクラス・要素**:

| セレクタ | 説明 |
|---|---|
| `:root` | フォントファミリー（`Noto Sans JP`）、カラースキームの設定 |
| `body` | グラデーション背景（紫系）、中央寄せグリッドレイアウト |
| `.app-shell` | 最大幅 960px のコンテナ |
| `.app-card` | 白背景のカード（角丸 28px、影付き、最小高さ 640px） |
| `.app-header h1` | タイトル |
| `.status-label` | 現在のモードラベル |
| `.status-time` | 残り時間表示 |
| `.app-actions` | ボタンコンテナ（flexbox、ギャップ 12px） |

---

## HTML テンプレート

### index.html

**パス**: `templates/index.html`

ポモドーロタイマーのメイン画面テンプレート。

**構造**:

```
<main class="app-shell">
  <section class="app-card">
    <header class="app-header">          ← タイトル表示
    <section class="app-status">         ← モード・残り時間表示（静的表示）
    <section class="app-actions">        ← 開始・リセットボタン
  </section>
</main>
<script id="initial-settings" ...>       ← JSON 設定の埋め込み
<script type="module" src="timer-ui.js"> ← JS エントリポイント
```

**注意**: 現時点のタイマー表示（「作業中」「25:00」）は静的なテキストであり、JavaScript による動的更新は未実装。
