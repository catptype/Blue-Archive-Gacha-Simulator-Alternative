import { createApp } from 'vue'
import { createPinia } from 'pinia'
import VueApexCharts from "vue3-apexcharts"; 
import './style.css'
import App from './App.vue'
import router from './router'

const app = createApp(App);
const pinia = createPinia();

app.use(router);
app.use(pinia);
app.use(VueApexCharts);

app.mount('#app');