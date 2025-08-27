<script setup>
// URLの?mode=condo を見て入力フォームを切替
import { computed, ref, reactive } from 'vue'
import ModeSelector from '@/components/ModeSelector.vue';
import RentInputs from '@/components/RentInputs.vue';
import OwnerInputs from '@/components/OwnerInputs.vue';
import CondoInputs from '@/components/CondoInputs.vue';
import YearlyTable from '@/components/YearlyTable.vue';

const params = new URLSearchParams(location.search)
const mode = ref(params.get('mode') === 'condo' ? 'condo' : 'owner')
const showCondo = computed(() => mode.value === 'condo')
const results = reactive({
    rent: null,
    owner: null,
    condo: null,
})

// 子からのemitを受け取るハンドラ
function onRentDone(payload) { results.rent = payload }
function onOwnerDone(payload) { results.owner = payload }
function onCondoDone(payload) { results.condo = payload }
</script>

<template>
    <div class="container">
        <h1>賃貸 vs 持ち家 シミュレーター</h1>
        <ModeSelector />

        <div class="grid">
            <RentInputs @done="onRentDone" />
            <OwnerInputs v-if="!showCondo" @done="onOwnerDone" />
            <CondoInputs v-else @done="onCondoDone" />
        </div>
        <!-- <div v-if="!showCondo" class="grid">
            <RentInputs />
            <OwnerInputs />
        </div>
        <div v-else class="grid">
            <RentInputs />
            <CondoInputs />
        </div> -->

        <YearlyTable />
        <YearlyTable v-if="results.rent" :title="賃貸" :rows="results.rent.rows" />
        <YearlyTable v-if="results.owner && !showCondo" :title="持ち家" :rows="results.owner.rows" />
        <YearlyTable v-if="results.condo && showCondo" :title="分譲マンション" :rows="results.condo.rows" />
    </div>
</template>

<style>
.container { padding: 16px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
</style>
