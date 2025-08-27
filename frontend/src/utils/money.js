export function yen(n) {
  const v = Number(n || 0)
  return '¥' + v.toLocaleString('ja-JP')
}
