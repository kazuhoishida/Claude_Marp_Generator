# スライド生成システム

ラフな原稿から、体裁の整ったスライドを作る。
出力は markdown と、そこから書き出す PDF / PowerPoint。
レンダリングは [Marp](https://marp.app/)。

## セットアップ

```bash
npm install
```

Node.js が必要。PDF と png の書き出しに使う Chromium は marp-cli が
自動で用意するので、個別のインストールは要らない。

写真や動画を貼る場合、PowerPoint を書き出す場合は、下記も入れる。

| 用途 | 必要なもの |
| --- | --- |
| 画像・動画の変換（`tools/`） | `brew install ffmpeg` |
| 文字を編集できる PowerPoint | `brew install --cask libreoffice` |
| PowerPoint の後処理（`tools/embed_videos.py`） | `pip install python-pptx` |

## 使い方

### 1. 原稿を置く

`input/` にラフな状態で置く。箇条書き・議事録・メモのままでよい。
体裁を整えるのはこのシステムの仕事。

書いてあると精度が上がるもの:

- 聞き手は誰か
- 聞き手に何をしてほしいか
- 使いたい画像があればそのパス

### 2. スライドにする

Claude Code に依頼する。ルールは `CLAUDE.md` にあり、読んでから作る。

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

### 4. 書き出す

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

## 素材の準備

原稿に付いてくる写真や動画は、そのままではスライドに使えない。
`tools/` のスクリプトで整える。

```bash
# 画像を縮小する（長辺1400pxまで。トリミングはしない）
python3 tools/prepare_images.py output/assets/<デッキ名> path/to/*.jpg

# 動画を720pのmp4にして、静止画も書き出す（最後の数字は静止画を取る位置）
tools/convert_video.sh in.mov output/assets/<デッキ名>/in.mp4 poster.png 0.5
```

動画は PDF には入らない。スライドには静止画を貼り、PPTX にだけ動画を
埋め込む。どのスライドにどの動画を入れるかは、素材ディレクトリに
`videos.json` を置いて指定する。

```json
{
  "4": ["in.mp4", "poster.png"],
  "7": ["other.mp4", "other_poster.png"]
}
```

キーはスライド番号（1始まり）、値は `[動画, ポスターに使う静止画]`。

```bash
python3 tools/embed_videos.py output/<デッキ名>.pptx
```

素材ディレクトリは既定で `output/assets/<pptx と同じ名前>` を見る。
別の場所なら `--assets` で渡す。

このスクリプトは動画の埋め込みだけでなく、`pptx-editable` の変換で崩れる
次の3つも直す。PDF 経由で変換する仕組み上、避けられない副作用のため。

- 白いだけの全面シェイプが全ページに3枚重なる
- 1行ごとに別のテキストボックスに分かれ、編集しても文章が流れ直さない
- テキストボックスの幅が行の文字数任せになり、左右が非対称に見える

## ディレクトリ

```
CLAUDE.md              作業の流れとスライド作成ルール（体裁・中身）
YYYYMMDD_template.md   テンプレート兼・記法の見本
themes/theme.css       テーマ。見た目の定義はすべてここ
.claude/commands/      スラッシュコマンド（/create-slides）
.vscode/settings.json  VS Code の Marp 拡張にテーマを教える設定
tools/                 素材の準備と pptx の後処理
  prepare_images.py      画像の縮小
  convert_video.sh       動画の mp4 変換 + 静止画の書き出し
  embed_videos.py        pptx への動画埋め込みとテキストの整形
.images/               テンプレートで使うプレースホルダー画像
input/                 入力（ラフな原稿）
output/                出力（.md / .pdf / .pptx と素材）
resources/             参照用の過去記事・既存資料
```

`input/` `output/` `resources/` の中身と、書き出した PDF は git で追跡しない。
このリポジトリは「仕組みと見た目」のマスターとして扱い、
個々の原稿やスライドは入れない。

## テーマ

テーマ名は `custom-deck`。front-matter に `theme: custom-deck` と書く。

見た目の調整は `themes/theme.css` に入れる。
markdown の front-matter に `style:` を書いて個別に上書きしない
（デッキごとに見た目がずれていく）。

配色はグレースケール + アクセント1色。見出しにも色は付けない。
カード・数値・手順・コールアウトの部品を用意してあるので、
箇条書きだけで埋めずに使い分ける。

使えるレイアウトと部品は [CLAUDE.md](CLAUDE.md) の「体裁のルール」を参照。

## 画像アセット

`.images/` はテンプレートが使うプレースホルダー置き場。
本番の図版ができたら**同名で上書きする**（参照側を変えずに済む）。

- `figure_sample.png` — 図版のダミー（テンプレートの `figure-full` で使用）
- `background.png` — 現在どこからも参照していない。背景画像は使わない方針

再生成は `npm run assets`（`.images/generate_placeholders.py`）。
標準ライブラリだけで動くので追加インストールは要らない。

デッキごとの写真・動画はここではなく `output/assets/<デッキ名>/` に置く。

## 見本

[YYYYMMDD_template.md](YYYYMMDD_template.md) が唯一の見本。使える記法と
レイアウトが1枚ずつ入っていて、コピーして書き始める下敷きも兼ねる。
`/create-slides` もこれを読む。

**中身の作り方**（構成の型・見出しの立て方）は見本ではなく
[CLAUDE.md](CLAUDE.md) の「中身のルール」を見る。

PDF はリポジトリに含めていない。テーマを変えると見本の方が古くなり、
直したはずの見た目と食い違うため。見た目を確認するときは書き出す。

```bash
npm run pdf -- YYYYMMDD_template.md
```
