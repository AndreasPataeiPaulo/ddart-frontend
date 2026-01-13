import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Homeview.vue'
import ProcessView from '../views/ProcessView.vue' // new screen
import DRProcess from '../views/DRProcess.vue'   
const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/process', name: 'Process', component: ProcessView },
  {
    path: '/dr-process',
    name: 'DRProcess',
    component: DRProcess
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router