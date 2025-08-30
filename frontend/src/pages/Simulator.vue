<script setup>
// URLの?mode=condo を見て入力フォームを切替
import { computed, ref, reactive } from 'vue'
import { yen } from '../utils/money.js'
import ModeSelector from '@/components/ModeSelector.vue';
import RentInputs from '@/components/RentInputs.vue';
import OwnerInputs from '@/components/OwnerInputs.vue';
import CondoInputs from '@/components/CondoInputs.vue';
import YearlyTable from '@/components/YearlyTable.vue';

const horizonYears = ref(35)

const params = new URLSearchParams(location.search)
const mode = ref(params.get('mode') === 'condo' ? 'condo' : 'owner')
const showCondo = computed(() => mode.value === 'condo')

const results = reactive({ rent: null, owner: null, condo: null })

const rentRef = ref(null)
const ownerRef = ref(null)
const condoRef = ref(null)

function submitAll() {
    rentRef.value?.submit(horizonYears.value)
    if (showCondo.value) {
        condoRef.value?.submit(horizonYears.value)
    } else {
        ownerRef.value?.submit(horizonYears.value)
    }
}

// 子からのemitを受け取るハンドラ
function onRentDone(payload) { results.rent = payload }
function onOwnerDone(payload) { results.owner = payload }
function onCondoDone(payload) { results.condo = payload }

function pickAnnual(row) {
    return (
        Number(row?.total_cost_year) ??
        Number(row?.total) ??
        Number(row?.year_total) ??
        0
    )
}

// n年目の行を取得
function getNthYearRow(rows, n) {
    if (!Array.isArray(rows) || rows.length === 0 || !Number.isFinite(n)) return null
    const byYear = rows.find(r => Number(r?.year) === n)
    if (byYear) return byYear
    const idx = Math.max(0, Math.min(rows.length - 1, n - 1))
    return rows[idx] ?? rows[rows.length - 1]
}

// 賃貸サマリー（n年目の毎月、年間、n年間の総額）
const rentSummary = computed(() => {
    const rows =results.rent?.rows
    if (!Array.isArray(rows) || rows.length === 0) return null

    const n = Number(horizonYears.value)
    const nthRow = getNthYearRow(rows, n)
    if (!nthRow) return null

    const annualN = pickAnnual(nthRow)
    const monthlyN = annualN / 12

    // 先頭〜n年目までの総額（行数がn未満ならある分だけ合算）
    const upto = Math.min(n, rows.length)
    let totalNYears = 0
    for (let i = 0; i < upto; i++) {
        totalNYears += pickAnnual(rows[i])
    }

    return {
        monthlyFinal: monthlyN,
        annualFinal: annualN,
        totalNYears: totalNYears,
    }
})
</script>

<template>
    <div class="container">
        <h1>賃貸 vs 持ち家 シミュレーター</h1>
        <ModeSelector v-model="mode"/>

        <div class="grid">
            <!-- <RentInputs @done="onRentDone" /> -->
            <RentInputs ref="rentRef" :horizon-years="horizonYears" @done="onRentDone" />
            <OwnerInputs v-if="!showCondo" ref="ownerRef" :horizon-years="horizonYears" @done="onOwnerDone" />
            <CondoInputs v-else  ref="condoRef" :horizon-years="horizonYears" @done="onCondoDone" />
        </div>

        <div class="controls">
            <label>
                期間（年）
                <input type="number"  min="1" step="1" v-model.number="horizonYears">
            </label>
            <button @click="submitAll">両方計算</button>
        </div>

        <table v-if="rentSummary" class="summary-table">
            <thead>
                <tr>
                    <th></th>
                    <th>支払家賃</th>
                    <th>住宅ローン返済額</th>
                    <th>差額</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{{ horizonYears }}年目の毎月支払額</td>
                    <td>{{ yen(rentSummary.monthlyFinal) }}</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>{{ horizonYears }}年目の年間支払額</td>
                    <td>{{ yen(rentSummary.annualFinal) }}</td>
                    <td></td>
                    <td></td>
                </tr>
                <tr>
                    <td>{{ horizonYears }}年間の支払総額</td>
                    <td>{{ yen(rentSummary.totalNYears) }}</td>
                    <td></td>
                    <td></td>
                </tr>
            </tbody>
        </table>

        <div class="tables">
            <YearlyTable v-if="results.rent" :title="'賃貸'" :rows="results.rent.rows" />
            <YearlyTable v-if="results.owner && !showCondo" :title="'持ち家(戸建)'" :rows="results.owner.rows" />
            <YearlyTable v-if="results.condo && showCondo" :title="'分譲マンション'" :rows="results.condo.rows" />
        </div>
    </div>
</template>

<style>
.container { padding: 16px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
</style>
