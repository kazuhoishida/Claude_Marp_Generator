# スライド生成システム

ラフな原稿を渡すと、体裁の整ったスライドを作る。
出力は markdown と、そこから書き出す PDF / PowerPoint。
レンダリングは [Marp](https://marp.app/)。

## セットアップ

```bash
npm install
```

写真・動画を扱う場合と、PowerPoint を書き出す場合は追加で入れる。

```bash
brew install ffmpeg                  # 画像・動画の変換
brew install --cask libreoffice      # 文字を編集できる PowerPoint
pip install python-pptx              # PowerPoint への動画埋め込み
```

## 使い方

### 1. 原稿を置く

`input/` にラフな状態で置く。箇条書き・議事録・メモのままでよい。
体裁を整えるのはこのシステムの仕事。

書いてあると精度が上がるもの:

- 聞き手は誰か
- 聞き手に何をしてほしいか
- 使いたい画像があればそのパス

写真や動画は撮ったままのファイルでよい。スライドに載る大きさへの縮小や、
PowerPoint に入る形式への変換はこちらで行う。

### 2. スライドにする

Claude Code に依頼する。

```
/create-slides input/my-draft.md
```

構成を決めて markdown を書き、png に書き出して目視で確認し、
直してから PDF にするところまで続けて行う。

自分で markdown を書く場合は `YYYYMMDD_template.md` をコピーして
`output/` に置き、下のコマンドで書き出す。**png で確認してから PDF にする。**
CSS の効き方はレンダリングしないと分からず、画像のはみ出しやコードの
読みにくさは markdown を読んでいる限り気付けない。

## コマンド

| コマンド | 内容 |
| --- | --- |
| `npm run images -- <file>` | png で書き出す（確認用） |
| `npm run pdf -- <file>` | PDF を書き出す |
| `npm run pptx -- <file>` | PowerPoint を書き出す（各ページは画像。文字の編集は不可） |
| `npm run pptx-editable -- <file>` | 文字を編集できる PowerPoint を書き出す |
| `npm run preview` | ブラウザでライブプレビュー |

## 見た目を変える

見た目の定義は `themes/theme.css` にまとめてある。
markdown 側に `style:` を書いて個別に上書きしない（デッキごとにずれていく）。

使えるレイアウトと部品（カード・数値・手順・コールアウトなど）の一覧は
[CLAUDE.md](CLAUDE.md) の「体裁のルール」にある。

## 見本

[YYYYMMDD_template.md](YYYYMMDD_template.md) が唯一の見本。使える記法と
レイアウトが1枚ずつ入っていて、コピーして書き始める下敷きも兼ねる。

構成の型や見出しの立て方は [CLAUDE.md](CLAUDE.md) の「中身のルール」を見る。
