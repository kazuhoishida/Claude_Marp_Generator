---
description: input/ の原稿からスライドを作り、output/ に markdown と PDF を出力する
argument-hint: [入力ファイル] (省略時は input/ から探す)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# スライドを作る

入力: $ARGUMENTS （空なら `input/` の中を見て、対象をユーザーに確認する）

## 手順

1. **`CLAUDE.md` を最後まで読む。省略しない。**
   体裁（記法・レイアウト・配色・画像）と中身（構成・見出し・文章）の
   ルールがどちらもここに入っている。

2. 入力原稿を読む。`resources/` に関連しそうな資料があれば併せて読む。

3. 原稿に写真・動画が付いていたら、`tools/` で整えて
   `output/assets/<デッキ名>/` に置く。原寸のまま貼らない。

   ```bash
   python3 tools/prepare_images.py output/assets/<デッキ名> <画像...>
   tools/convert_video.sh <in.mov> output/assets/<デッキ名>/<名前>.mp4 <名前>.png
   ```

   動画は PDF に入らないので、スライドには静止画を貼る。

4. 構成を決める。書き始める前に、この3つを言語化して冒頭に示す。
   - 聞き手は誰か
   - 聞き手に何をしてほしいか
   - 一番伝えたいこと（1文）

   資料の種類（提案資料 / 手順書）で構成の型が変わる。判断がつかなければ聞く。

5. `YYYYMMDD_template.md` を下敷きに `output/<YYYYMMDD>_<名前>.md` を書く。
   - front-matter は `theme: custom-deck`
   - `style:` を front-matter に書かない
   - 画像パスは `output/` からの相対（`assets/<デッキ名>/foo.png`）

6. **png に書き出して目視確認する。**

   ```bash
   npm run images -- output/<ファイル名>.md
   ```

   書き出した png を Read ツールで実際に見る。最低限、
   **画像を含むスライド全部**と**コードブロックを含むスライド全部**を確認する。
   見るべき点:
   - 画像がスライドの端に触れていないか / はみ出していないか
   - コードの文字が背景に埋もれていないか
   - 本文が下端からはみ出していないか

7. 問題があれば直す。**文字を小さくして押し込むのではなく、スライドを分割する。**
   直したら 6 に戻ってもう一度見る。

8. 見た目が通ってから PDF にする。

   ```bash
   npm run pdf -- output/<ファイル名>.md
   ```

9. PowerPoint を求められたら書き出す。動画がある場合は、素材と同じ場所に
   `videos.json`（キーはスライド番号、値は `[動画, 静止画]`）を書いてから
   後処理を実行する。これをやらないと動画は入らず、テキストボックスも
   1行ごとに分かれたままになる。

   ```bash
   npm run pptx-editable -- output/<ファイル名>.md
   python3 tools/embed_videos.py output/<ファイル名>.pptx
   ```

10. 確認用に書き出した png を消す。

## 報告

完成したら、スライドの構成（見出しの一覧）と、原稿から補いきれず
`TODO:` を残した箇所を伝える。目視確認をどこまでやったかも書く。

原稿に無い情報を推測で埋めない。分からないものは `TODO:` にして聞く。
