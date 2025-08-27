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
    const acc = {}
    props.rows.forEach(r => {
        ALL_COLUMNS.forEach(c => {
            if (r[c.key] && Number(r[c.key]) !== 0) acc[c.key] = true
        })
    })
    acc['total_cost_year'] = true
    acc['cum_total_cost'] = true
    return ALL_COLUMNS.filter(c => acc[c.key])
})
</script>

<template>
    <div class="card">
        <h2>{{ title }}</h2>
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
                    <tr v-for="row in rows" :key="row.year">
                        <td>{{ row.year }}</td>
                        <td v-for="col in visibleCols" :key="col.key" :class="{ sticky: col.sticky }">
                            {{ yen(row[col.key]) }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<style>
.card { border:1px solid #ddd; border-radius:8px; padding:12px; margin-top:12px; }
.table-wrap { overflow-x:auto; }
table { width:100%; border-collapse: collapse; min-width: 720px; }
th, td { border-bottom:1px solid #eee; padding:6px 8px; text-align:right; }
th:first-child, td:first-child { text-align:center; }
th.sticky, td.sticky { font-weight:600; }
h2 { margin: 0 0 8px; }
</style>
