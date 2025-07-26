<template>
  <div class="home-container">
    <div class="header">
      <p>Logado como: <strong>{{ auth.email }}</strong></p>
      <p>Sessão expira em: <strong>{{ auth.getTokenExpiration() }}</strong></p>
      <button @click="auth.logout">Logout</button>
    </div>

    <h1>Coin Indicators</h1>

    <status-section :gecko-status="geckoStatus" :api-status="apiStatus" />
    <import-section :tempo="tempo" :import-message="importMessage" :import-error="importError" @importar="importar"
      @indicadores="indicadores" />


    <div class="filter">
      <label for="coin-filter">Filtrar por símbolo:</label>
      <select id="coin-filter" v-model="selectedSymbol">
        <option value="">Todas</option>
        <option v-for="coin in uniqueSymbols" :key="coin" :value="coin">
          {{ coin.toUpperCase() }}
        </option>
      </select>
    </div>

    <data-section :coins="filteredCoins" :indicators="filteredIndicators" />

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  getGeckoStatus,
  getTempoRestanteImportacao,
  importarMoedas
} from '../services/geckoService'
import {
  getStatus,
  getIndicadores
} from '../services/apiService'
import { useAuthStore } from '../store/auth'

import StatusSection from '../components/StatusSection.vue'
import ImportSection from '../components/ImportSection.vue'
import DataSection from '../components/DataSection.vue'

const auth = useAuthStore()

const apiStatus = ref('')
const geckoStatus = ref('')
const tempo = ref(null)
const importMessage = ref('')
const importError = ref('')

const coins = ref([])
const indicators = ref([])
const selectedSymbol = ref('')

const getGeckoApiStatus = async () => {
  try {
    const result = await getGeckoStatus()
    geckoStatus.value = result["gecko_says"]
  } catch {
    geckoStatus.value = ''
  }
}

const getApiStatus = async () => {
  try {
    const result = await getStatus()
    apiStatus.value = result
  } catch {
    apiStatus.value = ''
  }
}

const getTempo = async () => {
  try {
    tempo.value = await getTempoRestanteImportacao()
  } catch (err) {
    tempo.value = null
  }
}

const indicadores = async () => {
  try {
    const data = await getIndicadores()
    coins.value = data.coins
    indicators.value = data.coins_indicators
  } catch (err) {
    importError.value = err.response?.data?.detail || 'Erro ao importar moedas e indicadores'
  }
}

const importar = async () => {
  importMessage.value = ''
  importError.value = ''
  try {
    const result = await importarMoedas()
    importMessage.value = result.message
    await getTempo()
    await indicadores()
  } catch (err) {
    importError.value = err.response?.data?.detail || 'Erro ao consumir API CoinGecko'
  }
}

// Computa os símbolos únicos para popular o select
const uniqueSymbols = computed(() => {
  const symbolsSet = new Set(coins.value.map(c => c.symbol))
  return Array.from(symbolsSet).sort()
})

// Computa a lista filtrada pelo símbolo selecionado
const filteredCoins = computed(() => {
  if (!selectedSymbol.value) return coins.value
  return coins.value.filter(c => c.symbol === selectedSymbol.value)
})

// Computa a lista filtrada pelo símbolo selecionado
const filteredIndicators = computed(() => {
  if (!selectedSymbol.value) return indicators.value
  return indicators.value.filter(c => c.symbol === selectedSymbol.value)
})

onMounted(async () => {
  try {
    await getGeckoApiStatus()
    await getApiStatus()
    await getTempo()

    if (tempo.value?.pode_importar) {
      // Executa automaticamente se estiver liberado
      await importar()
    } else {
      // Apenas carrega os indicadores se já estiverem disponíveis
      await indicadores()
    }
  } catch (err) {
    console.error('Erro ao carregar dados iniciais:', err)
  }
})
</script>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background-color: #f6f9fc;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

section {
  margin-bottom: 30px;
}

button {
  padding: 10px 20px;
  background-color: #2d98da;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.msg {
  margin-top: 10px;
  font-size: 14px;
}

.success {
  color: green;
}

.error {
  color: red;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.data-section {
  display: flex;
  gap: 2rem;
}

.column {
  flex: 1;
}

.coin-card,
.indicator-card {
  border: 1px solid #ccc;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  background: #f9f9f9;
}

.filter {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

select {
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

</style>
