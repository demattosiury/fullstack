<template>
    <section class="status">
        <h2>Status da API</h2>
        <p>Conectado à CoinGeckoAPI:
            <span v-if="geckoStatus">✅</span>
            <span v-else><strong>Carregando...</strong></span>
        </p>
        <p>Health Check da API:
            <span v-if="apiStatus">✅</span>
            <span v-else><strong>Carregando...</strong></span>
        </p>
    </section>
</template>

<script setup>
defineProps({
    geckoStatus: String,
    apiStatus: String
})
</script>

<style scoped>
.status {
    margin-bottom: 30px;
}
</style>
