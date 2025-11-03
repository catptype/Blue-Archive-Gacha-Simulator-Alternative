import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/Home.vue';
import StudentView from '../views/Student.vue';
import LoginView from '../views/Login.vue';
import RegisterView from '../views/Register.vue';

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
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
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