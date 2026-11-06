#!/usr/bin/env node
/** 本地演示：用商品名称查条码 / 规格，或用条码反查详情。 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sample = path.join(root, 'data', 'products.sample.jsonl')

function loadProducts() {
  return fs.readFileSync(sample, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map((line) => JSON.parse(line))
}

function printItem(it) {
  const spec = (it.spec || []).join(' / ') || '-'
  console.log(`名称：${it.name}`)
  console.log(`条码：${it.barcode}`)
  console.log(`规格：${spec}`)
  if (it.category) console.log(`分类：${it.category}`)
  console.log()
}

const args = process.argv.slice(2)
const nameIdx = args.indexOf('--name')
const barcodeIdx = args.indexOf('--barcode')
const qName = nameIdx >= 0 ? args[nameIdx + 1] : ''
const qBarcode = barcodeIdx >= 0 ? args[barcodeIdx + 1] : ''

if (!qName && !qBarcode) {
  console.error('用法: node lookup.mjs --name 农夫山泉')
  console.error('      node lookup.mjs --barcode 6901209205606')
  process.exit(1)
}

const items = loadProducts()
const hits = qName
  ? items.filter((it) => it.name.includes(qName))
  : items.filter((it) => it.barcode === qBarcode)

console.log(`命中 ${hits.length} 条，展示前 ${Math.min(5, hits.length)} 条\n`)
hits.slice(0, 5).forEach(printItem)
