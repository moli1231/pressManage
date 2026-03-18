import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import LoginView from '../views/LoginView.vue'
import MainLayout from '../layouts/MainLayout.vue'
import DashboardView from '../views/DashboardView.vue'
import GaugeListView from '../views/GaugeListView.vue'
import UserManagementView from '../views/UserManagementView.vue'
import ReminderView from '../views/ReminderView.vue'
import ProfileView from '../views/ProfileView.vue'
import ImportExportView from '../views/ImportExportView.vue'

const routes = [
  { path: '/login', component: LoginView },
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', component: DashboardView },
      { path: 'gauges', component: GaugeListView },
      { path: 'users', component: UserManagementView, meta: { roles: ['admin', 'super'] } },
      { path: 'reminders', component: ReminderView, meta: { roles: ['admin', 'super'] } },
      { path: 'import-export', component: ImportExportView, meta: { roles: ['admin', 'super'] } },
      { path: 'profile', component: ProfileView },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const store = useAuthStore()
  if (to.path !== '/login' && !store.isLoggedIn) {
    return '/login'
  }
  if (to.path === '/login' && store.isLoggedIn) {
    return '/'
  }
  const roles = to.meta?.roles
  if (roles && !roles.includes(store.role)) {
    return '/'
  }
  return true
})

export default router
