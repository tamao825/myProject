# Morning Report

## 概要
毎朝、首都圏の鉄道運行情報と東京の天気を取得して Slack に通知する Python スクリプトです。

- Yahoo!路線情報（首都圏）の遅延・運休状況を取得
- OpenWeatherMap API から東京の天気を取得
- Slack Webhook 経由で通知

---

## ディレクトリ構成
myProject/
├─ morningReport/
│ ├─ morningReport.py # メインスクリプト
│ ├─ requirements.txt # 依存ライブラリ
│ ├─ webhook.env # Slack Webhook URL (git管理対象外)
| └─ README.md
└─ .github/
  └─ workflows/
  └─ morningReport.yml # GitHub Actions ワークフロー
