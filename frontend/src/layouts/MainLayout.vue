<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">PressureGauge CMS</div>
      <el-menu :default-active="activePath" router>
        <el-menu-item index="/">工作台</el-menu-item>
        <el-menu-item index="/gauges">压力表列表</el-menu-item>
        <el-menu-item v-if="canManageUsers" index="/users">用户管理</el-menu-item>
        <el-menu-item v-if="canSeeReminders" index="/reminders">到期提醒</el-menu-item>
        <el-menu-item v-if="canImportExport" index="/import-export">导入导出</el-menu-item>
        <el-menu-item index="/profile">个人中心</el-menu-item>
      </el-menu>
    </aside>
    <main class="content">
      <header class="header page-card">
        <div>欢迎，{{ auth.user?.phone }}（{{ auth.user?.role }}）</div>
        <el-button type="danger" plain @click="logout">退出登录</el-button>
      </header>
      <section>
        <router-view />
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const activePath = computed(() => route.path)
const canManageUsers = computed(() => ['admin', 'super'].includes(auth.role))
const canSeeReminders = computed(() => ['admin', 'super'].includes(auth.role))
const canImportExport = computed(() => ['admin', 'super'].includes(auth.role))

function logout() {
  auth.clearAuth()
  router.push('/login')
}
</script>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: 100vh;
}

.sidebar {
  background: linear-gradient(200deg, #0f4c81, #1e6ba8);
  padding: 20px 12px;
}

.brand {
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
}

.content {
  padding: 18px;
}

.header {
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-menu) {
  border-right: none;
  background: transparent;
}

:deep(.el-menu-item) {
  color: #e7f1ff;
  border-radius: 8px;
  margin: 4px 0;
}

:deep(.el-menu-item:hover),
:deep(.el-menu-item.is-active) {
  background: rgba(255, 255, 255, 0.18);
  color: #fff;
}

@media (max-width: 900px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    padding: 8px;
  }
}
</style>
