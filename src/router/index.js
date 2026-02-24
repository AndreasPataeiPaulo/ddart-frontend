import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Homeview.vue'
import ProcessView from '../views/ProcessView.vue' // new screen
import LoginView from '../views/LoginView.vue'
import DoctorView from '../views/DoctorView.vue'
import ResearchView from '../views/ResearchView.vue'



const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/', name: 'Home', component: HomeView },
  { path: '/process', name: 'Process', component: ProcessView },
  { path: '/doctor', name: 'Doctor', component: DoctorView },
  { path: '/research', name: 'Research', component: ResearchView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router