import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Homeview.vue'
import ProcessView from '../views/ProcessView.vue'
import LoginView from '../views/LoginView.vue'
import DoctorView from '../views/DoctorView.vue'
import ResearchView from '../views/ResearchView.vue'
import HealthCenterView from '../views/HealthCenterView.vue'
import StudyOfficialView from '../views/StudyOfficialView.vue'

const routes = [
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/', name: 'Home', component: HomeView },
  { path: '/process', name: 'Process', component: ProcessView },
  { path: '/doctor', name: 'Doctor', component: DoctorView, meta: { requiresDoctor: true } },
  { path: '/research', name: 'Research', component: ResearchView, meta: { requiresDoctor: true } },
  { path: '/health-center', name: 'HealthCenter', component: HealthCenterView, meta: { requiresHealthCenter: true } },
  { path: '/study', name: 'Study', component: StudyOfficialView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const patient = localStorage.getItem('ddart_patient')
  const doctor = localStorage.getItem('ddart_doctor')
  const healthCenter = localStorage.getItem('ddart_health_center')

  // Redirect logged-in users away from login page
  if (to.name === 'Login') {
    if (healthCenter) return next('/health-center')
    if (patient) return next('/')
    if (doctor) {
      const d = JSON.parse(doctor)
      return next(d.is_research ? '/research' : '/doctor')
    }
    return next()
  }

  // Protect health center routes
  if (to.meta.requiresHealthCenter) {
    if (!healthCenter) return next('/login')
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