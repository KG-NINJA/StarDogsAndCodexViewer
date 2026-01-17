# Codex Viewer Bridge (agentdogs)

Codex CLI の活動ログを `RTSagents` の `events.ndjson` に流し、
それを `codex-trace.json` に変換して `agentdogs/index.html` の
Codex Viewer にリアルタイム反映するための最小構成セットです。

## 目的
- Codex CLI の行動をゲーム画面に可視化
- 追加依存なし（Python 標準ライブラリのみ）
- ワンコマンドで自動起動

## 構成
- `index.html` : 3Dビューア本体（Codex Viewer モード対応）
- `rtsagents_to_codex_trace.py` : `events.ndjson` → `codex-trace.json` 変換ブリッジ
- `start_codex_viewer_bridge.sh` : ブリッジ2本まとめて起動
- `codex-trace.json` : ビューアが読むトレースファイル

前提: `RTSagents` ディレクトリが `/home/user/RTSagents` に存在すること

## クイックスタート

1) ブリッジ起動
```bash
/home/user/agentdogs/start_codex_viewer_bridge.sh
```

2) `index.html` をブラウザで開く

3) 右上 `Codex Viewer` に切り替える

4) `Watch File` をON

これで Codex CLI の動作が画面に反映されます。

## ログ
- `/home/user/RTSagents/bridge.log`
- `/home/user/agentdogs/trace_bridge.log`

## トラブルシュート

### 動かない
- `Watch File` が ON か確認
- `codex-trace.json` が更新されているか確認
- 上記ログにエラーがないか確認

### 長文が短くしか動かない
- `rtsagents_to_codex_trace.py` はメッセージを複数チャンクに分割してイベント化します。
  反映されない場合はブリッジを再起動してください。

## GitHub 公開時の注意
- パスは環境に合わせて書き換えてください（`/home/user` 固定）
- `RTSagents` が別の場所にある場合、`start_codex_viewer_bridge.sh` を編集してください

## ライセンス
MIT（`RTSagents` のライセンスに準拠）
