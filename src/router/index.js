import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Homeview.vue'
import ProcessView from '../views/ProcessView.vue' // new screen
<<<<<<< HEAD

=======
>>>>>>> 5450bfa (Initial upload of AI app with ONNX backend)
const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/process', name: 'Process', component: ProcessView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router