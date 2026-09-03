#!/bin/bash
# スライドで使う動画を mp4 に変換し、静止画（ポスターフレーム）を書き出す。
#
# PDF には動画が入らないので、スライドには静止画を貼り、PPTX にだけ動画を
# 埋め込む。iPhone で撮った .mov は 4K の HEVC で、PowerPoint（特に Windows）
# では再生できないことがあるため、720p の H.264 mp4 に落とす。
#
#   tools/convert_video.sh <入力.mov> <出力.mp4> [ポスター.png] [位置0.0-1.0]
#
# 位置は静止画を取り出す場所。既定は 0.5（真ん中）。動画の冒頭は動き出す前の
# ことが多いので、頭ではなく中間を既定にしている。
#
# 空間ビデオのように音声やメタデータのトラックが複数ある素材があるので、
# 映像1本 + 音声1本だけを明示的に選ぶ（-map）。回転情報は ffmpeg が自動で
# 適用するため、縦位置で撮った動画もそのままの向きで出る。
#
# 縮小は「長辺を1280に収める」。幅を基準にすると、縦位置で撮った動画が
# 1280x2276 のように縦に伸びた巨大なファイルになる。
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "usage: $0 <in.mov> <out.mp4> [poster.png] [at:0.0-1.0]" >&2
  exit 2
fi

src="$1"; out="$2"; poster="${3:-}"; at="${4:-0.5}"

dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")
seek=$(python3 -c "print(f'{float('$dur') * float('$at'):.2f}')")

ffmpeg -y -loglevel error -i "$src" \
  -map 0:v:0 -map 0:a:0? \
  -vf "scale='if(gte(iw,ih),min(1280,iw),-2)':'if(gte(iw,ih),-2,min(1280,ih))'" \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "$out"
echo "$out  $(du -m "$out" | cut -f1)MB  $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$out")"

if [ -n "$poster" ]; then
  ffmpeg -y -loglevel error -ss "$seek" -i "$src" -frames:v 1 "$poster"
  echo "$poster  $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$poster")"
fi
