import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# yahoo路線情報（首都圏）
train_url = "https://transit.yahoo.co.jp/traininfo/area/4/"

# Slack Webhook URL
webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

# ブラウザを模倣するUser-Agent（スクレイピング対策）
headers = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/115.0.0.0 Safari/537.36")
}

# Yahooの相対URLを絶対URLに変換するためのベースURL
base_url = "https://transit.yahoo.co.jp"  # 相対パスを補完するベースURL

# OpenWeatherMapのAPIKey
api_key = "6f060865f0f7460788ee15894a47ea2b"
city_name = "Tokyo"

def get_weather():
    # OpenWeatherMapのURL
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={api_key}"
    try:
        res = requests.get(weather_url, timeout=10)
        res.raise_for_status()
        data = res.json()
        description = data["weathet"][0]["description"]
        temp = ["main"]["temp"]
        return f"🌤 今日の天気: {description}, 気温: {temp}℃"
    except Exception as e:
        return f"❌ 天気情報取得エラー: {e}"




def get_train_status():
    """電車の遅延情報を取得して文字列で返却する。"""
    try:
        # ページ取得
        res = requests.get(train_url, headers=headers, timeout=10)
        res.encoding = res.apparent_encoding # 文字化け対策
        soup = BeautifulSoup(res.text, "html.parser")

        # 運行情報のテーブル行を取得
        rows = soup.select("div.elmTblLstLine table tr")
        if not rows:
            return "❌ 運行情報を取得できませんでした。"

        results = []
        for row in rows[1:]: # 1行目はヘッダなのでスキップ
            cols = row.find_all("td")
            if len(cols)<3:
                continue # 必要な列が揃っていない場合はスキップ

            # 路線名とリンク取得
            a_tag = cols[0].find("a")
            if a_tag:
                line_name = a_tag.get_text(strip=True)
                href = a_tag['href']
                # 相対URLを絶対URLに変換
                line_link = href if href.startswith("http") else base_url + href
                linked_line = f"<{line_link}|{line_name}>"  # Slack用リンク形式
            else:
                linked_line = cols[0].get_text(strip=True)
            # 運行状況と詳細取得
            status = cols[1].get_text(strip=True) # 状況
            detail = cols[2].get_text(strip=True) # 詳細

            # 平常運転でない場合のみメッセージ作成
            if status != "平常運転":
                results.append(f"\n⚠️{linked_line}: {status} - {detail}")

        # 異常がなければ平常運転メッセージ
        if results:
            return "\n".join(results)
        else:
            return "現在、運休や遅延はありません（平常運転）"
    except requests.exceptions.RequestException as e:
        return f"❌ 運行情報の取得に失敗しました: {e}"
    except Exception as e:
        return f"❌ 想定外のエラーが発生しました: {e}"

def send_slack(message: str):
    """slackにメッセージを送信する"""
    try:
        res = requests.post(webhook_url, json={"text": message}, timeout=10)
        res.raise_for_status  # 失敗したら例外を投げる
    except requests.exceptions.RequestException as e:
        print(f"Slack送信エラー: {e}")

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = get_train_status()
    # Slack通知用メッセージ作成
    report = f"📢 {now} 時点の運行情報\n{status}"
    print(report)
    send_slack(report)

if __name__ == "__main__":
    main()

def lambda_handler(event, context):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    status = get_train_status()
    # Slack通知用メッセージ作成
    report = f"📢 {now} 時点の運行情報\n{status}"
    send_slack(report)
    return {"status": "ok"}
