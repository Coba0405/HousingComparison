<script setup>
import { ref } from 'vue'

const params = new URLSearchParams(location.search)
const currentMode = ref(params.get('mode') || 'owner')

function goCondo() {
    const url = new URL(location.href)
    url.searchParams.set('mode', 'condo')
    location.href = url.toString()
}

function goOwner() {
    const url = new URL(location.href)
    url.searchParams.set('mode', 'owner')
    location.href = url.toString()
}
</script>

<template>
    <div style="display:flex; gap:8px; align-items:center;">
        <div v-if="currentMode === 'owner'">
            <button style="background:#2563eb;color:#fff; padding:6px 10px; border-radius:6px;" @click="goCondo">
                分譲マンションを選ぶ
            </button>
        </div>
        <div v-else-if="currentMode === 'condo'">
            <button style="background:#2563eb;color:#fff; padding:6px 10px; border-radius:6px;" @click="goOwner">
                戸建を選ぶ
            </button>
        </div>
    </div>
</template>
