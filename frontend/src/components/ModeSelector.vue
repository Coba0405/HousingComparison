<script setup>
function goCondo() {
    const url = new URL(location.href)
    url.searchParams.set('mode', 'condo')
    location.href = url.toString()
}
</script>

<template>
    <div style="display:flex; gap:8px; align-items:center;">
        <button>rent（賃貸）</button>
        <button>house（戸建）</button>
        <button style="background:#2563eb;color:#fff; padding:6px 10px; border-radius:6px;" @click="goCondo">
            分譲マンションを選ぶ
        </button>
    </div>
</template>
