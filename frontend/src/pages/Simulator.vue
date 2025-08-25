<script setup>
// URLの?mode=condo を見て入力フォームを切替
import { computed, ref } from 'vue'
import ModeSelector from '@/components/ModeSelector.vue';
import RentInputs from '@/components/RentInputs.vue';
import OwnerInputs from '@/components/OwnerInputs.vue';
import CondoInputs from '@/components/CondoInputs.vue';
import YearlyTable from '@/components/YearlyTable.vue';
import ModeSelector from '@/components/ModeSelector.vue';

const params = new URLSearchParams(location.search)
const mode = ref(params.get('mode') || 'default')
const showCondo = computed(() => mode.value === 'condo')
</script>

<template>
    <div class="container">
        <h1>賃貸 vs 持ち家 シミュレーター</h1>
        <ModeSelector />

        <div v-if="!showCondo" class="grid">
            <RentInputs />
            <OwnerInputs />
        </div>
        <div v-else>
            <CondoInputs />
        </div>

        <YearlyTable />
    </div>
</template>

<style>
.container { padding: 16px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
</style>
