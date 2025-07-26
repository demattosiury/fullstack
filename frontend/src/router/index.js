import { createRouter, createWebHistory } from 'vue-router'
import AuthLanding from '../pages/AuthLanding.vue'
import HomePage from '../pages/HomePage.vue'

const routes = [
  { path: '/', component: AuthLanding },
  { path: '/home', component: HomePage, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard global
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.path === '/' && token) {
    return next('/home')
  }

  if (to.meta.requiresAuth && !token) {
    return next('/')
  }

  next()
})

export default router