<script setup>
import { computed } from 'vue'
import { yen } from '../utils/money.js'

const props = defineProps({
    title: { type: String, default: '' },
    rows: { type: Array, default: () => [] }
})

const ALL_COLUMNS = [
    { key: 'rent',              label: '家賃(年合計)' },
    { key: 'renewal_fee',       label: '更新料' },
    { key: 'contents_insurance',label: '家財保険' },
    { key: 'loan_payment',      label: 'ローン返済(年合計)' },
    { key: 'fire_insurance',    label: '火災保険' },
    { key: 'property_taxes',    label: '固定資産税+都市計画税' },
    { key: 'house_renovation',  label: '修繕(戸建10年ごと)' },
    { key: 'mgmt_fee',          label: '管理費(分譲)' },
    { key: 'reserve_fee',       label: '修繕積立(分譲)' },
    { key: 'total_cost_year',   label: '年合計', sticky: true },
    { key: 'cum_total_cost',    label: '累計',   sticky: true },
]

const visibleCols = computed(() => {
    if (!props.rows?.length) return []
    const used = new Set()

    for (const r of props.rows) {
        for (const c of ALL_COLUMNS) {
        const v = r?.[c.key]
        if (typeof v === 'number' && v !== 0) used.add(c.key)
        }
    }
    used.add('total_cost_year')
    used.add('cum_total_cost')

    return ALL_COLUMNS.filter(c => used.has(c.key))
    })

    function fmt(value, key) {
    if (key === 'year') return String(value ?? '—')
    if (typeof value !== 'number') return '—'
    return yen(value)
}
</script>

<template>
    <div v-if="rows?.length" class="card">
        <h2 class="title">{{ title }}</h2>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>年</th>
                        <th v-for="col in visibleCols" :key="col.key" :class="{ sticky: col.sticky }">
                            {{ col.label }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(row, i) in rows" :key="row.year ?? i">
                        <td class="year-col">
                            {{ row.year }}
                        </td>
                        <td v-for="col in visibleCols" :key="col.key" :class="{ sticky: col.sticky }">
                            {{ fmt(row[col.key], col.key) }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <div v-else class="empty">データがありません</div>
</template>

<style scoped>
.card { border: 1px solid #ddd; border-radius: 8px; padding: 12px; margin-top: 12px; }
.title { margin: 0 0 8px; font-weight: 600; }
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; min-width: 760px; }
th, td { border-bottom: 1px solid #eee; padding: 6px 8px; text-align: right; }
.year-col { text-align: center; white-space: nowrap; }
th.sticky, td.sticky { font-weight: 700; }
.empty { margin-top: 12px; color: #666; }
</style>
