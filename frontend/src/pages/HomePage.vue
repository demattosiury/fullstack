<template>
  <div class="home-container">
    <div class="header">
      <span>Logado como: <strong>{{ auth.email }}</strong></span>
      <button @click="auth.logout">Logout</button>
    </div>

    <h1>Indicadores Cripto</h1>

    <section class="status">
      <h2>Status da API</h2>
      <p v-if="status">Conectado à GeckoCoinAPI: ✅</p>
      <p v-else>Carregando status...</p>
    </section>

    <section class="import">
      <h2>Importar Moedas</h2>
      <p v-if="tempo">
        Tempo restante: <strong>{{ tempo.tempo_restante }} min</strong><br />
        Pode importar: <strong>{{ tempo.pode_importar ? 'Sim' : 'Não' }}</strong>
      </p>
      <button @click="importar" :disabled="!tempo?.pode_importar">
        Importar Agora
      </button>
      <p class="msg success" v-if="importMessage">{{ importMessage }}</p>
      <p class="msg error" v-if="importError">{{ importError }}</p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  getGeckoStatus,
  getTempoRestanteImportacao,
  importarMoedas
} from '../services/geckoService'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()

const status = ref(false)
const tempo = ref(null)
const importMessage = ref('')
const importError = ref('')

onMounted(async () => {
  try {
    await getStatus()
    await getTempo()
  } catch (err) {
    console.error('Erro ao carregar dados iniciais:', err)
  }
})

const getStatus = async () => {
  try {
    await getGeckoStatus()
    status.value = true
  } catch {
    status.value = false
  }
}

const getTempo = async () => {
  try {
    tempo.value = await getTempoRestanteImportacao()
  } catch (err) {
    tempo.value = null
  }
}

const importar = async () => {
  importMessage.value = ''
  importError.value = ''
  try {
    const result = await importarMoedas()
    importMessage.value = result.message
    await getTempo()
  } catch (err) {
    importError.value = err.response?.data?.detail || 'Erro ao importar moedas'
  }
}
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
</style>
