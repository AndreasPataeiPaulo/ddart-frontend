import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Homeview.vue'
import ProcessView from '../views/ProcessView.vue' // new screen
import LoginView from '../views/LoginView.vue'
import DoctorView from '../views/DoctorView.vue'

// Add to routes array:

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/', name: 'Home', component: HomeView },
  { path: '/process', name: 'Process', component: ProcessView },
  { path: '/doctor', name: 'Doctor', component: DoctorView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router