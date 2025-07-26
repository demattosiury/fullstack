import api from './api'

export async function getStatus() {
  const response = await api.get('/status')
  return response.data
}

export async function getIndicadores() {
  const response = await api.get('/indicadores')
  return response.data
}