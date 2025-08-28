<script setup>
// URLの?mode=condo を見て入力フォームを切替
import { computed, ref, reactive } from 'vue'
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
