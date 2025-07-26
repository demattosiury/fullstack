<template>
  <section class="import">
    <h2>Importar Moedas</h2>
    <p v-if="tempo">
      Tempo restante: <strong>{{ tempoFormatado }}</strong><br />
      Pode importar: <strong>{{ canImport ? 'Sim' : 'Não' }}</strong>
    </p>

    <button @click="onImportar" :disabled="!canImport">
      Consumir API CoinGecko
    </button>

    <button @click="onIndicadores" :disabled="!canImport" style="margin-left: 10px;">
      Importar Moedas e Indicadores
    </button>

    <p class="msg success" v-if="importMessage">{{ importMessage }}</p>
    <p class="msg error" v-if="importError">{{ importError }}</p>
  </section>
</template>

<script setup>
import { ref, watch, onUnmounted, computed } from 'vue'

const props = defineProps({
  tempo: Object,
  importMessage: String,
  importError: String
})

const emit = defineEmits(['importar', 'indicadores'])

const onImportar = () => emit('importar')
const onIndicadores = () => emit('indicadores')

const tempoRestanteSegundos = ref(0)
const canImport = ref(false)
let intervalId = null

function formatarTempo(segundos) {
  const m = Math.floor(segundos / 60).toString().padStart(2, '0')
  const s = (segundos % 60).toString().padStart(2, '0')
  return `${m}:${s}`
}

function iniciarContagem() {
  if (!props.tempo || typeof props.tempo.waiting_time !== 'number') {
    tempoRestanteSegundos.value = 0
    canImport.value = true
    return
  }

  tempoRestanteSegundos.value = props.tempo.waiting_time
  canImport.value = false

  if (intervalId) clearInterval(intervalId)

  intervalId = setInterval(() => {
    if (tempoRestanteSegundos.value > 0) {
      tempoRestanteSegundos.value--
    } else {
      canImport.value = true
      clearInterval(intervalId)
    }
  }, 1000)
}

watch(() => props.tempo, () => {
  iniciarContagem()
}, { immediate: true })

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})

const tempoFormatado = computed(() => formatarTempo(tempoRestanteSegundos.value))
</script>

<style scoped>
.import {
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
</style>
