<script setup>
import { ref } from 'vue'
import { simulateCondo } from '../utils/api.js'

const form = ref({
    horizon_years: 10,
    region: '東京大都市部',
    rounding_rule: 'round',
    home_price: 30000000,
    loan_years: 35,
    loan_annual_rate: 0.012,
    mgmt_monthly0: 12000,
    reserve_monthly0: 10000,
    mgmt_increase_every_5y_pct: 0.10,
    reserve_increase_every_5y_pct: 0.20,
})

async function submit() {
    const res = await simulateCondo(form.value)
    console.log('condo result', res)
}
</script>

<template>
    <div class="card">
        <h2>分譲マンション 入力</h2>
        <label>管理費（月）<input type="number" v-model.number="form.mgmt_monthly0" /></label>
        <label>修繕積立金（月）<input type="number" v-model.number="form.reserve_monthly0" /></label>
        <label>修繕費 5年ごと増率<input type="number" step="0.01" v-model.number="form.mgmt_increase_every_5y_pct" /></label>
        <label>修繕積立金 5年ごと増率<input type="number" step="0.01" v-model.number="form.mgmt_increase_every_5y_pct" /></label>
        <button @click="submit">計算</button>
    </div>
</template>

<style>
.card { border:1px solid #ddd; border-radius:8px; padding:12px; }
label { display:block; margin:6px 0; }
</style>
