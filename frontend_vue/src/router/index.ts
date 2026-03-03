import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/home/Home.vue';
import StudentView from '@/views/student/Student.vue';
import GachaView from '@/views/gacha/Gacha.vue';
import LoginView from '@/views/user/Login.vue';
import RegisterView from '@/views/user/Register.vue';
import DashboardView from '@/views/user/Dashboard.vue';
import SummaryTab from '@/views/user/layout/SummaryTab.vue';
import HistoryTab from '@/views/user/layout/HistoryTab.vue';
import CollectionTab from '@/views/user/layout/CollectionTab.vue';
import AchievementsTab from '@/views/user/layout/AchievementsTab.vue';

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
    path: '/gacha',
    name: 'Gacha',
    component: GachaView,
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
  },
  {
    path: '/dashboard',
    component: DashboardView,
    // --- THIS IS THE NESTED ROUTING PART ---
    children: [
      { path: '', redirect: '/dashboard/summary' }, // Default redirect
      { path: 'summary', name: 'DashboardSummary', component: SummaryTab },
      { path: 'history', name: 'DashboardHistory', component: HistoryTab },
      { path: 'collection', name: 'DashboardCollection', component: CollectionTab },
      { path: 'achievements', name: 'DashboardAchievements', component: AchievementsTab },
    ]
  },


];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


export default router;