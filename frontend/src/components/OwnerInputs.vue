<script setup>
import { ref } from 'vue'
import { simulateHouse } from '../utils/api.js'

const form = ref({
    horizon_years: 10,
    region: '東京大都市部',
    rouding_rule: 'round',
    home_price: 30000000,
    loan_years: 35,
    loan_annual_rate: 0.012,
    fire_insurance_monthly: 1000,
    property_tax_charge_month: 12,
    house_renovation_every_10y_amount: 500000,
    house_renovation_charge_month: 12,
})

async function submit() {
    const res = await simulateHouse(form.value)
    console.log('house result', res)
}
</script>

<template>
    <div class="card">
        <h2>戸建 入力</h2>
        <label>比較年数<input type="number" v-model.number="form.horizon_years" /></label>
        <label> 地域<input v-model="form.region" /></label>
        <label>物件価格<input type="number" v-model.number="form.home_price" /></label>
        <label>年利（固定）<input type="number" step="0.001" v-model.number="form.loan_annual_rate" /></label>
        <label>10年ごとの修繕（円）<input type="number" v-model.number="form.house_renovation_every_10y_amount" /></label>
        <button @click="submit">計算</button>
    </div>
</template>

<style>
.card { border:1px solid #ddd; border-radius:8px; padding:12px; }
label { display:block; margin:6px 0; }
</style>
