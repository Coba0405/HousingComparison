<script setup>
import { ref } from 'vue'
import { simulateOwner } from '../utils/api.js'

const emit = defineEmits(['done'])
const props = defineProps({ horizonYears: { type: Number, required: true} })

const form = ref({
    horizon_years: 35,
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

const regionOptions = [
    { value: 'tokyo_core', label: '東京大都心部' },
    { value: 'kanto_dense', label: '関東地価集中地域' },
    { value: 'regional_city_dense', label: '地方都市地価集中地域' },
    { value: 'regional_dense', label: '地方地価集中地域' },
    { value: 'regional', label: '地方地域' },
    { value: 'depopulated', label: '地方過疎地域' },
]

async function submit(hYears = mergeProps.horizonYears) {
    const payload = {
        ...form.value,
        horizon_years: hYears,
    }
    const res = await simulateOwner(payload)
    emit('done', res)
}

defineExpose({ submit })
</script>

<template>
    <div class="card">
        <h2>戸建 入力</h2>
        <label>比較年数<input type="number" v-model.number="form.horizon_years" /></label>
        <label>地域
            <select v-model="form.region" class="border rounded px-2 py-1">
                <option value="">選択してください</option>
                <option v-for="opt in regionOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                </option>
            </select>
        </label>
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
