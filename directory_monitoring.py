import os
import argparse
import pickle
import logging
import time
from datetime import datetime
from plyer import notification

# ロガーの呼び出し元の名前をこのスクリプト名にする
logger = logging.getLogger(__file__)

# ファイルとタイムスタンプの辞書型作成関数
def file_dic(target_dir):
    f_list = os.listdir(target_dir)
    f_dic = {}
    for k in f_list:
        f_dic[k] = os.stat(os.path.join(target_dir, k)).st_mtime
    return f_dic

# 通知関数
def _notify(flist, info):
    notify_ls = []
    if len(flist) > 0:
        for file in flist:
            notify_ls.append(f"【{info}】 {file}")
    else:
        notify_ls.append(f"【{info}】 なし")
    return notify_ls

def notify_info(flist_list, target_dir):
    notify_list = []
    log_list = []
    status = ["追加", "削除", "変更"]
    for flist, stat in zip(flist_list, status):
        notify_list += [f"【{stat}】： {len(flist)} 件"]
        log_list += _notify(flist, stat)

    # windowsの通知に変更件数を表示する
    notification.notify(
        title=f"\"{target_dir}\" ディレクトリ変更情報",
        message="\n".join(notify_list),
        app_name="file_check"
    )
    # ログファイルに変更されたファイル名を記載
    logger.info("\n".join(log_list))

def main(target_dir):
    # ログの設定
    FORMAT = '%(asctime)-15s\n %(filename)s\n%(message)s'
    today = str(datetime.now().date())
    dir_name = os.path.basename(target_dir)
    logging.basicConfig(filename=today + "_" + dir_name + ".log",
                       level=logging.INFO,
                        format=FORMAT
                        )

    # 監視対象用のステータス保存ファイルパス
    status_file = os.path.join(target_dir + "_checklist")

    # 初期化
    if not os.path.exists(status_file):
        initlist = file_dic(target_dir)
        with open(status_file, "wb") as f:
            pickle.dump(initlist, f)

    # チェック
    filelist  = file_dic(target_dir)

    # 前回との差分を取り出す。
    if os.path.getsize(status_file) > 0:
        with open(status_file, "rb") as f:
            prevlist = pickle.load(f)
    else:
        prevlist = {}

    # 追加と移動を取り出す
    add_list = list(set(filelist) - set(prevlist))
    sub_list = list(set(prevlist) - set(filelist))

    # 最終更新日の変更をチェック
    modify_file = []
    for k1, k2 in zip(filelist, prevlist):
        if k1 == k2:
            if filelist[k1] != prevlist[k2]:
                modify_file.append(k1)

    # 差分に関してレポートする。
    # 追加、削除、変更の順にリストを作っていることに注意。
    notify_info([add_list, sub_list, modify_file], target_dir)

    # 状態ファイルの更新
    with open(status_file, "wb") as f:
        pickle.dump(filelist, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="指定したディレクトリ内のファイル変更を監視します。")

    parser.add_argument("target_dir", help="監視対象のディレクトリパスを設定")
    parser.add_argument("-mi", "--monitoring_interval",
                        help="監視をする時間間隔を設定(秒)",
                        type=int,
                        default=600)

    args = parser.parse_args()
    while True:
        main(args.target_dir)
        time.sleep(args.monitoring_interval)