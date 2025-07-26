<template>
    <section class="data-section">
        <div class="column">
            <h2>Moedas</h2>
            <ul>
                <li v-for="coin in coins" :key="coin.id" class="coin-card">
                    <img :src="coin.image" :alt="coin.name" width="32" />
                    <strong>{{ coin.name }}</strong> ({{ coin.symbol.toUpperCase() }}) Rank: {{ coin.market_cap_rank
                    }}<br />
                    Preço: U$ {{ coin.current_price.toLocaleString() }}<br />
                    Máxima 24h: U$ {{ coin.high_24h.toLocaleString() }}<br />
                    Mínima 24h: U$ {{ coin.low_24h.toLocaleString() }}<br />
                    Última atualização: {{ coin.last_updated.toLocaleString() }}
                </li>
            </ul>
        </div>

        <div class="column">
            <h2>Indicadores</h2>
            <ul>
                <li v-for="indicator in indicators" :key="indicator.coingecko_id" class="indicator-card">
                    <strong>{{ indicator.name }}</strong> ({{ indicator.symbol.toUpperCase() }})<br /><br /><br />
                    Distância do topo histórico: {{ indicator.percent_off_ath.toFixed(2) }}%<br />
                    Relação preço / menor valor 24h: {{ indicator.price_to_24h_low_ratio.toFixed(3) }}<br />
                    Volume / Market Cap: {{ indicator.volume_to_market_cap_ratio.toFixed(3) }}<br />
                    Dias desde ATH: {{ indicator.days_since_ath }}
                </li>
            </ul>
        </div>
    </section>
</template>

<script setup>
defineProps({
    coins: Array,
    indicators: Array
})
</script>

<style scoped>
.data-section {
    display: flex;
    justify-content: space-between;
    gap: 20px;
}

.column {
    flex: 1;
}

.coin-card,
.indicator-card {
    background-color: #fff;
    border: 1px solid #ddd;
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 6px;
}
</style>
