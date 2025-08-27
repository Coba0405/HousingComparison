<script setup>
import { ref } from 'vue'
import { simulateRent } from '../utils/api.js'

const emit = defineEmits(['done'])

const form = ref({
    horizon_years: 10,
    region: '東京大都市部',
    rounding_rule: 'round',
    rent_monthly: 100000,
    renewal_interval_years: 2,
    renewal_fee_amount: 50000,
    contents_insurance_amount: 20000,
})

async function submit() {
    try {
        const res = await simulateRent(form.value)
        emit('done', res)
    } catch (e) {
        console.log('simulateRent failed', e)
    }
}
</script>

<template>
    <div class="card">
        <h2>賃貸 入力</h2>
        <label>家賃（月）<input type="number" v-model.number="form.rent_monthly" /></label>
        <label>更新料（2年ごと）<input type="number" v-model.number="form.renewal_fee_amount" /></label>
        <label>家財保険（2年ごと）<input type="number" v-model.number="form.contents_insurance_amount" /></label>
        <button @click="submit">計算</button>
    </div>
</template>

<style>
.card { border:1px solid #ddd; border-radius: 8px; padding:12px; }
label { display:block; margin:6px 0; }
button { margin-top:8px; }
</style>
