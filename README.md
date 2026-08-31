# スライド生成システム

ラフな原稿から、体裁の整ったスライド（markdown + PDF）を作る。
レンダリングは [Marp](https://marp.app/)。

## セットアップ

```bash
npm install
```

Node.js が必要。PDF と png の書き出しには Chromium が使われるが、
marp-cli が自動で用意するので個別のインストールは要らない。

## 使い方

### 1. 原稿を置く

`input/` にラフな状態で置く。箇条書き・議事録・メモのままでよい。
体裁を整えるのはこのシステムの仕事。

書いてあると精度が上がるもの:

- 聞き手は誰か
- 聞き手に何をしてほしいか
- 使いたい画像があればそのパス

### 2. スライドにする

Claude Code / Cursor に依頼する。ルールは `.cursor/rules/` にあり、
エージェントはそれを読んでから作る。

```
/create-slides input/my-draft.md
```

手で書く場合は `YYYYMMDD_template.md` をコピーして `output/` に置く。

### 3. 確認する

**必ず png に書き出して目で見る。** CSS の効き方は
レンダリングしないと分からない。

```bash
npm run images -- output/20260829_my-deck.md
```

特に次の2つは markdown を読んでいる限り気付けない。

- 画像がスライド下端からはみ出す
- コードの文字色が背景に埋もれる

### 4. PDFにする

```bash
npm run pdf -- output/20260829_my-deck.md
```

## コマンド

| コマンド | 内容 |
| --- | --- |
| `npm run images -- <file>` | png で書き出す（確認用） |
| `npm run pdf -- <file>` | PDF を書き出す |
| `npm run pptx -- <file>` | PowerPoint を書き出す（各ページは画像。文字の編集は不可） |
| `npm run pptx-editable -- <file>` | 文字を編集できる PowerPoint を書き出す（LibreOffice が要る） |
| `npm run html -- <file>` | HTML を書き出す |
| `npm run preview` | ブラウザでライブプレビュー |
| `npm run assets` | プレースホルダー画像を再生成 |

`--theme-set themes/` と `--allow-local-files` は npm script に含めてある。
`marp` を直接叩くときは自分で付ける。付け忘れるとテーマが当たらない、
またはローカル画像が読み込まれない。

## ディレクトリ

```
.claude/commands/      スラッシュコマンド
.cursor/rules/         スライド作成ルール
  slide_rules.mdc        記法・レイアウト・配色・画像
  compelling-content.mdc 構成・見出し・文章
.images/               背景・図版
themes/theme.css       テーマ。見た目の定義はすべてここ
input/                 入力（ラフな原稿）
output/                出力（.md と .pdf）
resources/             参照用の過去記事・既存資料
YYYYMMDD_template.md   テンプレート
CLAUDE.md              Claude Code 向けの指示
```

## テーマ

テーマ名は `custom-deck`。front-matter に `theme: custom-deck` と書く。

見た目の調整は `themes/theme.css` に入れる。
markdown の front-matter に `style:` を書いて個別に上書きしない
（デッキごとに見た目がずれていく）。

使えるレイアウトは
[.cursor/rules/slide_rules.mdc](.cursor/rules/slide_rules.mdc) を参照。

## 画像アセット

`.images/` はプレースホルダー置き場。本番の図版ができたら
**同名で上書きする**（参照側を変えずに済む）。

- `figure_sample.png` — 図版のダミー（テンプレートの `figure-full` で使用）
- `background.png` — 現在どこからも参照していない。背景画像は使わない方針

`generate_placeholders.py` は標準ライブラリだけで動く。
差し替え後は不要なので消してよい。

## 見本

[YYYYMMDD_template.md](YYYYMMDD_template.md) が唯一の見本。使える記法と
レイアウトが1枚ずつ入っていて、コピーして書き始める下敷きも兼ねる。
`/create-slides` もこれを読む。

**中身の作り方**（構成の型・見出しの立て方）は見本ではなくルールを見る。
[.cursor/rules/compelling-content.mdc](.cursor/rules/compelling-content.mdc)。

PDF はリポジトリに含めていない。テーマを変えると見本の方が古くなり、
直したはずの見た目と食い違うため。見た目を確認するときは書き出す。

```bash
npm run pdf -- YYYYMMDD_template.md
```
