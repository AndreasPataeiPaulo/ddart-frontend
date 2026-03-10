import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HealthCenterView from '../views/HealthCenterView.vue'
import ResearchView from '../views/ResearchView.vue'
import StudyOfficialView from '../views/StudyOfficialView.vue'
import AdminView from '../views/AdminView.vue'

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: LoginView },
    { path: '/health-center', component: HealthCenterView },
    { path: '/research', component: ResearchView },
    { path: '/study', component: StudyOfficialView },
    { path: '/admin', component: AdminView },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
