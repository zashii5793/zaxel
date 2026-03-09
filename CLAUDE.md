# ZAXEL プロジェクト - Claude Code ガイド

## プロジェクト概要

github.com/zashii5793/zaxel のプロジェクト管理を Claude Code + GitHub Projects で自動化する。

---

## GitHub Projects カンバン構成

| カラム | 意味 | 使い方 |
|--------|------|--------|
| Backlog | 未着手・優先度未定 | Issue作成直後はここ |
| Ready | 着手可能・優先度確定済み | 次のスプリントで着手するもの |
| In Progress | 作業中 | 担当者アサイン済み |
| Done | 完了 | PRマージ or クローズ済み |

---

## よく使うコマンド

次のタスクを確認する: 次は何をすべきか教えて
議事録からIssueを作成する: 以下の議事録をもとにGitHub Issueを作成して
Issueのステータス更新: Issue #[番号] を In Progress に移動して
Issueを作成: [タイトル]というIssueを作成して
現在の進捗確認: カンバンの現状を教えて

---

## ラベル一覧

feature: 新機能 / bug: バグ修正 / docs: ドキュメント / refactor: リファクタリング / urgent: 緊急対応

---

## 議事録 → Issue 変換ルール

議事録フォーマット: 日時・参加者・決定事項・アクションアイテム（担当者・内容・期日）
Claude はアクションアイテムを優先的にIssue化し、担当者・期日をメタデータとして付与する。

---

## GitHub CLI コマンド早見表

gh issue list
gh issue create --title "タイトル" --body "内容" --label "feature"
gh issue close [番号]
gh project list
gh project item-list [project-number] --owner zashii5793

---

## 運用フロー

打ち合わせ → 議事録をClaude Codeに渡す → Issue自動提案・確認・修正
→ GitHubに登録（Backlog） → 次は何をすべきか？と聞く
→ ReadyのIssueを提案 → In Progressへ → 作業完了 → Done & PRマージ
