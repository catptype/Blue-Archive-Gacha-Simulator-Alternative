import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/Home.vue';
import StudentView from '@/views/Student.vue';
import GachaView from '@/views/Gacha.vue';
import LoginView from '@/views/Login.vue';
import RegisterView from '@/views/Register.vue';
import DashboardView from '@/views/Dashboard.vue';
import SummaryTab from '@/components/dashboard/SummaryTab.vue';
import HistoryTab from '@/components/dashboard/HistoryTab.vue';
import CollectionTab from '@/components/dashboard/CollectionTab.vue';
import AchievementsTab from '@/components/dashboard/AchievementsTab.vue';

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