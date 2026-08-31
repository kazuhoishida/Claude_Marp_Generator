#!/usr/bin/env python3
"""プレースホルダーの画像アセットを生成する。

本番の背景・図版が用意できるまでの仮素材。差し替えるときは
同名のファイルを上書きするだけでよい（参照側は変わらない）。

標準ライブラリだけで動く。実行:
    python3 .images/generate_placeholders.py
"""

import os
import struct
import zlib

ACCENT = (43, 108, 176)
FG = (36, 41, 47)
HERE = os.path.dirname(os.path.abspath(__file__))

# 図形のエッジを滑らかにするための超過サンプリング倍率
SS = 3


def write_png(path, width, height, rows, alpha=False):
    """RGB/RGBA のピクセル行を PNG として書き出す。

    rows は 1 行ぶんの bytes を並べたリスト。
    """
    color_type = 6 if alpha else 2
    raw = b"".join(b"\x00" + row for row in rows)  # フィルタタイプ 0

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )
    with open(path, "wb") as f:
        f.write(png)


def make_background(width=2560, height=1440):
    """白から極淡い青へ落とす縦グラデーション。文字が乗る前提で低コントラストに。"""
    rows = []
    bar = 14 * (height // 720)  # 下端のアクセント帯
    for y in range(height):
        if y >= height - bar:
            rows.append(bytes(ACCENT) * width)
            continue
        t = y / height
        px = bytes((int(255 - 12 * t), int(255 - 8 * t), int(255 - 3 * t)))
        rows.append(px * width)
    write_png(os.path.join(HERE, "background.png"), width, height, rows)


def _rounded_rect_hit(x, y, box, radius):
    """半径 radius で角を丸めた矩形の内側かどうか。

    矩形を radius だけ内側に縮めた領域への最近点距離で判定する。
    角の外側だけが radius より遠くなる。
    """
    x0, y0, x1, y1 = box
    if not (x0 <= x <= x1 and y0 <= y <= y1):
        return False
    nx = min(max(x, x0 + radius), x1 - radius)
    ny = min(max(y, y0 + radius), y1 - radius)
    return (x - nx) ** 2 + (y - ny) ** 2 <= radius ** 2


def _render_shapes(width, height, shapes):
    """shapes = [(box, radius, rgb)] を SS 倍で描いて縮小し、RGBA 行を返す。"""
    rows = []
    inv = 1.0 / (SS * SS)
    for y in range(height):
        row = bytearray()
        for x in range(width):
            acc_r = acc_g = acc_b = acc_a = 0.0
            for sy in range(SS):
                py = y + (sy + 0.5) / SS
                for sx in range(SS):
                    px = x + (sx + 0.5) / SS
                    for box, radius, rgb in shapes:
                        if _rounded_rect_hit(px, py, box, radius):
                            acc_r += rgb[0]
                            acc_g += rgb[1]
                            acc_b += rgb[2]
                            acc_a += 255
                            break
            if acc_a == 0:
                row += b"\x00\x00\x00\x00"
            else:
                # 色は被覆部分の平均、アルファは被覆率
                n = acc_a / 255
                row += bytes((int(acc_r / n), int(acc_g / n), int(acc_b / n),
                              int(acc_a * inv)))
        rows.append(bytes(row))
    return rows


def make_figure_sample(width=900, height=540):
    """図版のダミー。薄グレーの地に箱を並べた、図解を模したもの。"""
    shapes = [
        ((60, 60, 380, 200), 12, ACCENT),
        ((520, 60, 840, 200), 12, (120, 128, 138)),
        ((60, 260, 840, 300), 6, FG),
        ((60, 350, 380, 480), 12, (120, 128, 138)),
        ((520, 350, 840, 480), 12, ACCENT),
        ((0, 0, width, height), 0, (240, 243, 246)),  # 地。最後に置いて残りを埋める
    ]
    write_png(os.path.join(HERE, "figure_sample.png"), width, height,
              _render_shapes(width, height, shapes), alpha=True)


if __name__ == "__main__":
    make_background()
    print("background.png")
    make_figure_sample()
    print("figure_sample.png")
