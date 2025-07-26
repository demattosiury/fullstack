<template>
  <div class="auth-container">
    <div class="auth-panel login-panel">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <input v-model="loginEmail" type="email" placeholder="Email" />
        <input v-model="loginPassword" type="password" placeholder="Senha" />
        <button type="submit">Entrar</button>
        <p v-if="loginError" class="error">{{ loginError }}</p>
      </form>
    </div>

    <div class="auth-panel register-panel">
      <h2>Registro</h2>
      <form @submit.prevent="handleRegister">
        <input v-model="registerEmail" type="email" placeholder="Email" />
        <input v-model="registerPassword" type="password" placeholder="Senha" />
        <input v-model="registerConfirm" type="password" placeholder="Confirme a senha" />
        <button type="submit">Registrar</button>
        <p v-if="registerError" class="error">{{ registerError }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const loginEmail = ref('')
const loginPassword = ref('')
const loginError = ref('')
const registerEmail = ref('')
const registerPassword = ref('')
const registerConfirm = ref('')
const registerError = ref('')
const auth = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  loginError.value = ''
  try {
    await auth.login({ email: loginEmail.value, password: loginPassword.value })
    router.push('/home')
  } catch {
    loginError.value = 'Email ou senha inválidos.'
  }
}

const handleRegister = async () => {
  registerError.value = ''
  if (registerPassword.value !== registerConfirm.value) {
    registerError.value = 'Senhas não coincidem.'
    return
  }

  try {
    await auth.register({ email: registerEmail.value, password: registerPassword.value })
    router.push('/home')
  } catch {
    registerError.value = 'Erro ao registrar. Verifique os dados.'
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  min-height: 100vh;
}

.auth-panel {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background-color: #ffffff;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.05);
}

.login-panel {
  background-color: #f5f6fa;
}

.register-panel {
  background-color: #e3e7ed;
}

input {
  margin: 10px 0;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 100%;
}

button {
  margin-top: 10px;
  padding: 12px;
  background-color: #2d98da;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #2275b8;
}

.error {
  color: red;
  font-size: 14px;
  margin-top: 8px;
}
</style>
