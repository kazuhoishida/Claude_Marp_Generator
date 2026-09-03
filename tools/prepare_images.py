#!/usr/bin/env python3
"""スライドで使う画像を適切なサイズに落とす。

入力の写真は 4000px 以上あることが多く、そのまま貼ると PDF も PPTX も
無駄に重くなる。スライドは 1280x720 で、図版の表示幅は最大でも約 1000px
なので、長辺 1400px あれば足りる（PDF の拡大表示や印刷を考えて 1.4 倍）。

トリミングはしない。構図を変えると原稿の意図とずれるため、縮小だけする。

    python3 tools/prepare_images.py <出力先> <画像...> [--max 1400]

出力先に元のファイル名で書き出す。`--name` を付けると1枚だけ改名できる。
ffmpeg が要る（`brew install ffmpeg`）。
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_MAX = 1400


def size_of(path):
    """画素サイズを ffprobe で読む。"""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0:s=x", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    w, h = out.split("x")[:2]
    return int(w), int(h)


def main():
    ap = argparse.ArgumentParser(description="スライド用に画像を縮小する")
    ap.add_argument("dest", type=Path, help="出力先ディレクトリ")
    ap.add_argument("images", type=Path, nargs="+", help="元の画像")
    ap.add_argument("--max", type=int, default=DEFAULT_MAX, help="長辺の上限px")
    ap.add_argument("--name", help="出力ファイル名（画像を1枚だけ渡すとき）")
    args = ap.parse_args()

    if args.name and len(args.images) != 1:
        sys.exit("--name は画像1枚のときだけ使える")

    args.dest.mkdir(parents=True, exist_ok=True)

    for src in args.images:
        if not src.exists():
            sys.exit(f"見つからない: {src}")
        out = args.dest / (args.name or src.name)
        w, h = size_of(src)
        if max(w, h) <= args.max:
            shutil.copyfile(src, out)          # すでに小さいものはそのまま
            print(f"{out.name}  {w}x{h}（変更なし）")
            continue

        # 長辺を --max に合わせる。短辺は -1 で比率を保って自動計算させる。
        scale = f"scale={args.max}:-1" if w >= h else f"scale=-1:{args.max}"
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
             "-vf", scale, "-q:v", "2", str(out)],
            check=True)
        nw, nh = size_of(out)
        print(f"{out.name}  {w}x{h} -> {nw}x{nh}")


if __name__ == "__main__":
    main()
