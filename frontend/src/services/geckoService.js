import api from './api'

export async function getGeckoStatus() {
  const response = await api.get('/gecko/status')
  return response.data
}

export async function getTempoRestanteImportacao() {
  const response = await api.get('/gecko/tempo-importar')
  return response.data
}

export async function importarMoedas() {
  const response = await api.post('/gecko/importar')
  return response.data
}