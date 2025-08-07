export function convertCurrency(amount, fromCode, toCode, quotes) {
  if (fromCode === toCode) return amount

  const base = 'EUR'

  if (fromCode === base && quotes[`${base}${toCode}`]) {
    return amount * quotes[`${base}${toCode}`]
  }

  if (toCode === base && quotes[`${base}${fromCode}`]) {
    return amount / quotes[`${base}${fromCode}`]
  }

  if (quotes[`${base}${fromCode}`] && quotes[`${base}${toCode}`]) {
    const inBase = amount / quotes[`${base}${fromCode}`]
    return inBase * quotes[`${base}${toCode}`]
  }

  throw new Error(`Missing exchange rate for ${fromCode} → ${toCode}`)
}
