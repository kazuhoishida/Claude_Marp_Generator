# CLAUDE.md

Marp によるスライド生成システム。ラフな原稿を入力として受け取り、
体裁の整ったスライド（markdown + PDF）を出力する。

## ディレクトリ

```
.claude/commands/      スラッシュコマンド
.cursor/rules/         スライド作成の詳細ルール（後述。必ず読む）
.images/               背景・図版などの画像アセット
themes/theme.css       カスタムテーマ。見た目の定義はすべてここ
input/                 入力（ラフな原稿・議事録・箇条書きメモ）
output/                出力（完成した .md と .pdf）
resources/             参照用の過去記事・ブログ・既存資料
YYYYMMDD_template.md   スライドのテンプレート
```

## ルールの所在

体裁と中身のルールは `.cursor/rules/` にある。**スライドを作る前に必ず読む。**

- `.cursor/rules/slide_rules.mdc` — 記法・レイアウト・配色・画像の制約
- `.cursor/rules/compelling-content.mdc` — 構成・見出し・文章の作り方

内容をここに再掲しない。二重管理になって必ずずれる。

## 基本の流れ

1. `input/` の原稿を読む。無ければユーザーに元ネタを聞く
2. `resources/` に関連資料があれば目を通す
3. 上の2つのルールファイルを読む
4. `YYYYMMDD_template.md` を下敷きに `output/<日付>_<名前>.md` を書く
5. **png に書き出して目視で確認する**（下記）
6. 問題があれば直して再確認。直ってから PDF にする

## ビルド

`marp` は devDependency。初回だけ `npm install` する。

```bash
npm install                              # 初回のみ
npm run images -- output/foo.md          # png で書き出して目視確認
npm run pdf    -- output/foo.md          # PDF を出力
npm run pptx   -- output/foo.md          # PowerPoint を出力（各ページは画像）
npm run pptx-editable -- output/foo.md   # 文字を編集できる PowerPoint（LibreOffice が要る）
npm run preview                          # ブラウザでライブプレビュー
npm run assets                           # プレースホルダー画像を再生成
```

`--theme-set themes/` と `--allow-local-files` は npm script に入れてある。
`marp` を直接叩くときは自分で付ける。付け忘れるとテーマが当たらない、
またはローカル画像が読み込まれない。

## 確認を省略しない

**markdown を書いただけで「できました」と報告しない。**
CSS の効き方はレンダリングしないと分からない。特に次の2つは
markdown を読んでいる限り気付けない:

- 画像がスライド下端からはみ出す
- コードの文字色が背景に埋もれる

`npm run images` で png を書き出し、Read ツールで実際に見る。
少なくとも「画像を含むスライド全部」と「コードブロックを含むスライド全部」は見る。

## 見た目を直すとき

調整は `themes/theme.css` に入れる。markdown の front-matter に `style:` を
書いて個別に上書きしない。1枚だけの例外は `<!-- _class: ... -->` で対応する。

テーマ名は `custom-deck`。front-matter は `theme: custom-deck`。

## 画像アセット

`.images/` はプレースホルダー置き場。本番の図版が用意できたら
**同名で上書きする**（参照側を変えずに済む）。

- `figure_sample.png` — 図版のダミー（テンプレートの `figure-full` で使用）
- `background.png` — 現在どこからも参照していない。背景画像は使わない方針

再生成は `npm run assets`（`.images/generate_placeholders.py`）。
標準ライブラリだけで動くので追加インストールは要らない。

## 入力に無いことを書かない

原稿に無い数値・パス・チャンネル名・製品名を推測で補完しない。
埋めるべき箇所は `TODO:` を残してユーザーに聞く。
スライドは後から参照される資料なので、もっともらしい嘘が一番害になる。
