#! /usr/bin/env python3
# このファイルは、asset/minecraft以下にある
# modelとtextureの紐づけリストを作成するためのスクリプトです。
# 相対パスでassetのディレクトリを指定しているので、toolsディレクトリで下記のように実行してください。
# python ./check_model_json.py

import glob
import json
import re

# ところどころに出てくる、re.sub(r"\\", "/", ....)  は
# Windowsで実行した際にパスの区切りが "\" になるので "/" になおしています。
# したがって Mac / Linux 環境の場合は意味のない処理です。

# ./asset/minecraft/models 以下にある全jsonファイルのリストを作成
jsonlist = glob.glob("../assets/minecraft/models/**/*.json", recursive=True)

# textureのパスをkey, modelのjsonパスをvalueでもつ辞書
tex_list = {}

# minecraft独自のtextureリストを読み込む
original_tex_list = open("original_tex_list.txt")
line = original_tex_list.readline()
while line:
    key = re.sub("\n", "", line)
    tex_list[key] = []
    line = original_tex_list.readline()

# assets/minecraft/textures以下のpngファイルを全検索してtex_listに追加
for texpath in glob.glob("../assets/minecraft/textures/**/*.png", recursive=True):
    tex_filename = re.sub(r"\\", "/", re.sub("..\/assets\/minecraft\/textures\\\\", "", texpath))
    key = re.sub("\.png$", "", tex_filename)
    tex_list[key] = []

# 各モデル(json)が参照しているtextureのリストをCSV形式で出力
model_tex_list = open("model_tex_list.csv", "w")
error_tex_list = open("error_tex_list.csv", "w")
for filepath in jsonlist:
    with open(filepath, encoding="utf-8") as f:
        model_data = json.load(f)
        if model_data["textures"]:
            textures = model_data["textures"].values()
            model_tex_list.write(re.sub(r"\\", "/", filepath) + "," + ",".join(textures) + "\n")

            # 各モデル(json)に書かれているtexture名をkeyにしてtex_listにモデルのファイルパスを追加
            for texture in textures:
                if texture in tex_list:
                    tex_list[texture].append(filepath)
                else:   # tex_listに当該keyがない状態＝モデル(JSON)に書いてあるtextureへのパスが異なるまたは存在しない場合
                    print(texture ," is not found in tex_list. please check ", filepath)
                    error_tex_list.write(texture + "," + re.sub(r"\\", "/", filepath) + "," + "\n")
                    tex_list[texture] = [filepath]

# 各textureが参照されているモデル(json)のリストをCSV形式で出力
tex_model_list = open("tex_model_list.csv", "w")
for tex, path in tex_list.items():
    if len(path) > 0:
        tex_model_list.write(tex + "," + re.sub(r"\\", "/", ",".join(path)) + "\n")
    else:
        tex_model_list.write(tex + "\n")

