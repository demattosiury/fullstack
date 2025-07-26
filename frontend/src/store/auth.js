import { defineStore } from 'pinia'
import { login, register } from '../services/authService'
import router from '../router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null
  }),
  actions: {
    async login({ email, password }) {
      const data = await login(email, password)
      this.token = data.access_token
      localStorage.setItem('token', this.token)
      this.decodeEmail()
    },
    async register({ email, password, api_key }) {
      const data = await register(email, password, api_key)
      this.token = data.access_token
      localStorage.setItem('token', this.token)
      this.decodeEmail()
    },
    logout() {
      this.token = null
      this.email = null
      localStorage.removeItem('token')
      router.push('/')
    },
    decodeEmail() {
      try {
        const payload = JSON.parse(atob(this.token.split('.')[1]))
        this.email = payload.sub
      } catch {
        this.email = null
      }
    },
    getTokenExpiration() {
      if (!this.token) return null
      try {
        const payload = JSON.parse(atob(this.token.split('.')[1]))
        if (!payload.exp) return null
        return new Date(payload.exp * 1000)
      } catch (e) {
        return null
      }
    }
  }
})
