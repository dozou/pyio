# これは何？

竹村研究室振動班による竹村研究室振動班のための研究支援ツールです  

以下が想定の使用用途です．  

* 実験データの取得
* デモの作成
* 取得データの確認及び検証

# Requirement

基本的にはPython3が動く環境であれば大丈夫です．
以下は動作確認環境になります．

* Python3 with pip (Recommended version is over 3.7)
* MacOS or Linux(Ubuntu, Arch)

# Installation

    pip3 install git+https://[USERS]@bitbucket.org/kamoryo/pybration_v1.git --upgrade --user

## First Settings.

テキストエディタを用いて　`~/.pybration/param.json` を編集します．

    "System": {
        "param_format_version": "0.0.1",
        "setting_folder": "~/.pybration/",
        "plugin_folder": [],
        "work_folder": ""
    },

`"plugin_folder: []"` に任意のプラグインを設置するディレクトリを指定してください.  

e.g.)  

   `plugins_dolder: ["~/pybration_plugins"]`

**注意：""ダブルクォーテーションで必ず囲むこと**  

同様に`"work_folder": ""`もディレクトリパスの設定を行うことで実験データの書き出しや，プラグインから参照を行うことが可能です．  


# Create plugin

ターミナル上で `pyb_create` を実行するとプラグインを作成するツールが立ち上がります．
plugin_name，author，ボタンを使うのかどうか聞かれるので，それに回答します．
回答したら，自分が打った情報のプラグインのディレクトリが出来るので，それを自分で最初に決めたプラグインを設置するディレクトリに入れます．
最後に `Pybration` を起動するとさっき作ったプラグインのボタンが出来ているはずです．
**出来ていなければ，何かがおかしいので頑張ってください．

# Documents



### ライセンスとか ###
 
基本竹村研究室に属します．
ボスの意向に従って下さい．
