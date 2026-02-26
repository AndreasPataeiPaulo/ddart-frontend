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
router.beforeEach((to, from, next) => {
  const patient = localStorage.getItem('ddart_patient')
  const doctor = localStorage.getItem('ddart_doctor')

  // Redirect logged-in users away from login page
  if (to.name === 'Login') {
    if (patient) return next('/')
    if (doctor) {
      const d = JSON.parse(doctor)
      return next(d.is_research ? '/research' : '/doctor')
    }
    return next()
  }

  // Protect patient routes
  if (to.meta.requiresPatient) {
    if (!patient) return next('/login')
    return next()
  }

  // Protect doctor routes
  if (to.meta.requiresDoctor) {
    if (!doctor) return next('/login')
    return next()
  }

  next()
})


export default router