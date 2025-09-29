import os
import shutil
from datetime import datetime

# スクショが保存されている元フォルダ
src = "C:\\Users\\sodech\\Pictures\\Screenshots"

# 移動先のフォルダ（日付ごとにフォルダ作成）
dst = "C:\\Users\\sodech\\Pictures\\Screenshots\\SortByDate"

# srcフォルダ内のファイルをチェック
move_count = 0
for file in os.listdir(src):
    if file.startswith("スクリーンショット") and file.endswith(".png"):
        file_path = os.path.join(src, file)

        # ファイルの作成日時取得
        created_time = os.path.getctime(file_path)
        date_str = datetime.fromtimestamp(created_time).strftime("%Y-%m-%d")

        # 作成日ごとのフォルダ作成
        target_folder = os.path.join(dst, date_str)
        os.makedirs(target_folder, exist_ok= True)

        # ファイルを移動
        shutil.move(file_path, os.path.join(target_folder, file))
        move_count += 1

print(f"{move_count}件のファイルを移動しました！")