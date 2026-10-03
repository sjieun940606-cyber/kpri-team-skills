"""흰 배경 캐릭터 시트에서 인물·얼굴을 하나씩 오려 투명 PNG로 저장한다.

Canva 무료 요금제는 투명 배경 PNG를 내보낼 수 없어서, 흰 배경 PNG를 받아 여기서 배경을 지운다.
가장자리에 이어진 흰색만 지우므로 눈 흰자·옷의 흰 무늬는 남는다.

    python cutout.py 하루_시트.png -o assets/haru
    python cutout.py 하루_시트.png -o assets/haru --white 230 --min-area 0.004

결과: 조각마다 part-01.png …, 번호를 붙인 미리보기 preview.png
필요한 것: pip install pillow numpy
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def remove_white_background(img, white):
    """가장자리에서 이어진 흰 영역만 투명하게 만든다."""
    rgb = np.asarray(img.convert("RGB")).astype(np.int16)
    near_white = (rgb >= white).all(axis=2)
    h, w = near_white.shape

    # 흰 픽셀만 255인 마스크에서 가장자리의 흰 점을 씨앗으로 채운다.
    mask = Image.fromarray(np.where(near_white, 255, 0).astype(np.uint8)).copy()  # copy: 배열과 메모리를 나누면 채우기가 안 먹는다
    seeds = [(x, 0) for x in range(w)] + [(x, h - 1) for x in range(w)]
    seeds += [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)]
    for x, y in seeds:
        if mask.getpixel((x, y)) == 255:
            ImageDraw.floodfill(mask, (x, y), 128)

    background = np.asarray(mask) == 128
    rgba = np.asarray(img.convert("RGBA")).copy()
    rgba[background, 3] = 0
    return Image.fromarray(rgba), ~background


def find_parts(foreground, min_area, pad):
    """서로 떨어진 그림 덩어리(전신·얼굴 하나하나)의 상자를 찾는다.

    빠르게 하려고 가로 약 400칸 격자로 줄여서 덩어리를 찾은 뒤 원래 크기로 되돌린다.
    """
    h, w = foreground.shape
    s = max(1, w // 400)
    gh, gw = -(-h // s), -(-w // s)
    padded = np.zeros((gh * s, gw * s), dtype=bool)
    padded[:h, :w] = foreground
    grid = padded.reshape(gh, s, gw, s).any(axis=(1, 3))

    seen = np.zeros_like(grid)
    boxes = []
    for gy, gx in zip(*np.nonzero(grid)):
        if seen[gy, gx]:
            continue
        stack, cells = [(gy, gx)], 0
        seen[gy, gx] = True
        y0, x0, y1, x1 = gy, gx, gy, gx
        while stack:
            cy, cx = stack.pop()
            cells += 1
            y0, x0, y1, x1 = min(y0, cy), min(x0, cx), max(y1, cy), max(x1, cx)
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < gh and 0 <= nx < gw and grid[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        if cells * s * s < min_area * h * w:
            continue
        boxes.append([x0 * s, y0 * s, (x1 + 1) * s - 1, (y1 + 1) * s - 1])

    boxes = merge_overlapping(boxes, pad)
    boxes = [[max(0, x0 - pad), max(0, y0 - pad), min(w, x1 + pad + 1), min(h, y1 + pad + 1)] for x0, y0, x1, y1 in boxes]
    # 위 줄부터, 같은 줄은 왼쪽부터
    row = max(1, h // 8)
    return sorted(boxes, key=lambda b: (b[1] // row, b[0]))


def merge_overlapping(boxes, pad):
    """가까이 붙은 상자(삐친 머리카락, 손 등)는 한 조각으로 합친다."""
    merged = True
    while merged:
        merged = False
        out = []
        while boxes:
            a = boxes.pop()
            for b in boxes[:]:
                if a[0] - pad <= b[2] and b[0] - pad <= a[2] and a[1] - pad <= b[3] and b[1] - pad <= a[3]:
                    a = [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]
                    boxes.remove(b)
                    merged = True
            out.append(a)
        boxes = out
    return boxes


def save_preview(img, boxes, path):
    preview = img.convert("RGB").copy()
    draw = ImageDraw.Draw(preview)
    width = max(2, img.width // 400)
    try:
        font = ImageFont.load_default(size=max(16, img.width // 40))
    except TypeError:  # Pillow 10.1 이전
        font = ImageFont.load_default()
    for i, (x0, y0, x1, y1) in enumerate(boxes, 1):
        draw.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(232, 74, 74), width=width)
        draw.text((x0 + width * 3, y0 + width * 2), str(i), fill=(232, 74, 74), font=font)
    preview.save(path)


def main():
    p = argparse.ArgumentParser(description="흰 배경 캐릭터 시트를 투명 PNG 조각으로 오리기")
    p.add_argument("sheet", help="Canva에서 받은 흰 배경 PNG")
    p.add_argument("-o", "--out", default="cutout", help="저장 폴더")
    p.add_argument("--white", type=int, default=235, help="이 값 이상이면 흰 배경으로 본다 (0~255)")
    p.add_argument("--min-area", type=float, default=0.003, help="이보다 작은 조각(전체 넓이 비율)은 버린다")
    p.add_argument("--pad", type=int, default=6, help="조각 둘레 여백(px)")
    args = p.parse_args()

    img = Image.open(args.sheet)
    cut, foreground = remove_white_background(img, args.white)
    boxes = find_parts(foreground, args.min_area, args.pad)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for i, box in enumerate(boxes, 1):
        cut.crop(box).save(out / f"part-{i:02d}.png")
    save_preview(img, boxes, out / "preview.png")
    print(f"{len(boxes)}개 조각 → {out}/part-01.png …  번호 확인: {out}/preview.png")


if __name__ == "__main__":
    main()
