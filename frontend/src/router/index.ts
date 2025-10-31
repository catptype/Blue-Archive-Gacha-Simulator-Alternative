import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/Home.vue';
import StudentView from '../views/Student.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/student',
    name: 'Student',
    component: StudentView,
  }
  // {
  //   path: '/student',
  //   name: 'Student',
  //   // This is how you'll add other pages later
  //   component: () => import('@/views/StudentView.vue'),
  // },
  // {
  //   path: '/gacha',
  //   name: 'Gacha',
  //   component: () => import('@/views/GachaView.vue'),
  // },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;