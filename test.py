import subprocess
import os
import datetime

def get_recently_updated_files(directory, date):
    file_list = []
    threshold_date = datetime.datetime.strptime(date, "%Y-%m-%d")  # 指定日をdatetimeオブジェクトに変換

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))  # ファイルの更新日を取得

            if file_mtime > threshold_date:
                file_list.append(file_path)

    return file_list

# 使用例
def main():
    directory_path = "/Users/sayoko/Library/CloudStorage/GoogleDrive-discegaudere.blackberry@gmail.com/.shortcut-targets-by-id/1y2EPu-MP7p0VnvN1BS7HH86_bqE_Z9cG/土器実測自動化/docs"
    date = "2023-05-27"

    recently_updated_files = get_recently_updated_files(directory_path, date)
    # print(recently_updated_files)

    # files = ['/Users/sayoko/Library/CloudStorage/GoogleDrive-discegaudere.blackberry@gmail.com/.shortcut-targets-by-id/1y2EPu-MP7p0VnvN1BS7HH86_bqE_Z9cG/土器実測自動化/docs/20230506-B03-01/01_pcd_file_color.html']

    for file in recently_updated_files:
        # ファイルをステージングエリアに追加
        result = file.replace(directory_path, "")

        subprocess.call(['git', 'add', file])
        
        # ステージングエリアに追加したファイルをコミット
        subprocess.call(['git', 'commit', '-m', '自動コミット：{}'.format(file)])
        
        # リモートリポジトリにプッシュ
        process = subprocess.Popen(['git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()  # コマンドの実行結果を取得
        
        if process.returncode == 0:
            print('{result}プッシュが正常に完了しました。')
        else:
            print('プッシュ中にエラーが発生しました。')
            print('標準出力:', stdout)
            print('標準エラー:', stderr)

    print('すべてのコミット＆プッシュが完了しました。')

if __name__ == '__main__':
    main()