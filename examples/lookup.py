#!/usr/bin/env python3
"""本地演示：用商品名称查条码 / 进货渠道价 / 规格，或用条码反查详情。"""
import argparse
import json
from pathlib import Path

SAMPLE = Path(__file__).resolve().parents[1] / 'data' / 'products.sample.jsonl'


def load_products():
    items = []
    with SAMPLE.open(encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def by_name(items, q):
    q = q.strip().lower()
    return [it for it in items if q in it['name'].lower()]


def by_barcode(items, q):
    q = q.strip()
    return [it for it in items if it['barcode'] == q]


def print_item(it):
    spec = ' / '.join(it.get('spec') or []) or '-'
    print(f"名称：{it['name']}")
    print(f"条码：{it['barcode']}")
    print(f"进货渠道价：{it['channel_price']}")
    print(f"规格：{spec}")
    if it.get('category'):
        print(f"分类：{it['category']}")
    print()


def main():
    parser = argparse.ArgumentParser(description='左邻右舍商品资料样本查询')
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--name', help='按商品名称查询（支持部分匹配）')
    g.add_argument('--barcode', help='按商品条码查询')
    parser.add_argument('--limit', type=int, default=5)
    args = parser.parse_args()

    items = load_products()
    hits = by_name(items, args.name) if args.name else by_barcode(items, args.barcode)
    print(f'命中 {len(hits)} 条，展示前 {min(args.limit, len(hits))} 条\n')
    for it in hits[: args.limit]:
        print_item(it)


if __name__ == '__main__':
    main()
