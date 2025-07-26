<template>
  <section class="import">
    <h2>Importar Moedas</h2>
    <p v-if="tempo">
      Tempo restante: <strong>{{ tempo.tempo_restante }} min</strong><br />
      Pode importar: <strong>{{ tempo.pode_importar ? 'Sim' : 'Não' }}</strong>
    </p>

    <button @click="onImportar" :disabled="!tempo?.pode_importar">
      Consumir API CoinGecko
    </button>

    <button @click="onIndicadores" :disabled="!tempo?.pode_importar" style="margin-left: 10px;">
      Importar Moedas e Indicadores
    </button>

    <p class="msg success" v-if="importMessage">{{ importMessage }}</p>
    <p class="msg error" v-if="importError">{{ importError }}</p>
  </section>
</template>

<script setup>
defineProps({
  tempo: Object,
  importMessage: String,
  importError: String
})

defineEmits(['importar', 'indicadores'])

const onImportar = () => {
  // Emite evento para o componente pai
  emit('importar')
}

const onIndicadores = () => {
  emit('indicadores')
}
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
