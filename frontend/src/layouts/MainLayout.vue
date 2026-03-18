<template>
  <div class="admin-shell">
    <header class="topbar">
      <div class="system-title">压力表管理系统</div>
      <div class="topbar-right">
        <span class="phone">{{ auth.user?.phone }}</span>
        <button class="text-link" @click="router.push('/profile')">修改密码</button>
        <el-button round class="topbar-logout" @click="logout">退出</el-button>
      </div>
    </header>

    <div class="shell-body">
      <aside class="sider">
        <el-menu :default-active="activePath" router>
          <el-menu-item index="/">工作台</el-menu-item>
          <el-menu-item index="/gauges">压力表列表</el-menu-item>
          <el-menu-item v-if="canManageUsers" index="/users">账号管理</el-menu-item>
          <el-menu-item v-if="canSeeReminders" index="/reminders">到期提醒</el-menu-item>
          <el-menu-item v-if="canImportExport" index="/import-export">导入导出</el-menu-item>
          <el-menu-item index="/profile">个人中心</el-menu-item>
        </el-menu>

        <div class="sider-footer">
          <div class="current-user">当前：{{ auth.user?.phone || '-' }}</div>
          <el-button class="full-logout" round @click="logout">退出登录</el-button>
        </div>
      </aside>

      <main class="main-content">
        <div class="main-inner">
          <router-view />
        </div>
      </main>
    </div>
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
.admin-shell {
  min-height: 100vh;
  background: #f3f4f6;
}

.topbar {
  height: 64px;
  border-bottom: 1px solid #e6e8ec;
  background: #f6f7f9;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.system-title {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  letter-spacing: 1px;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
  color: #6b7280;
}

.phone {
  font-size: 15px;
}

.text-link {
  border: 0;
  background: transparent;
  color: #111827;
  font-size: 14px;
  cursor: pointer;
}

.topbar-logout {
  border-color: #d1d5db;
  color: #111827;
}

.shell-body {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: calc(100vh - 64px);
}

.sider {
  border-right: 1px solid #e6e8ec;
  background: #f7f7f8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px 10px 10px;
}

:deep(.el-menu) {
  border-right: 0;
  background: transparent;
}

:deep(.el-menu-item) {
  height: 44px;
  line-height: 44px;
  border-radius: 10px;
  margin-bottom: 8px;
  color: #1f2937;
  font-size: 16px;
  font-weight: 600;
  padding-left: 16px !important;
}

:deep(.el-menu-item:hover) {
  background: #eceef1;
  color: #111827;
}

:deep(.el-menu-item.is-active) {
  background: #e5e7eb;
  color: #111827;
}

.sider-footer {
  border-top: 1px solid #e5e7eb;
  padding-top: 12px;
}

.current-user {
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 10px;
}

.full-logout {
  width: 100%;
  border-color: #d1d5db;
  color: #111827;
}

.main-content {
  padding: 28px;
}

.main-inner {
  max-width: 980px;
  margin: 0 auto;
}

@media (max-width: 900px) {
  .topbar {
    padding: 0 12px;
  }

  .system-title {
    font-size: 20px;
  }

  .shell-body {
    grid-template-columns: 1fr;
  }

  .sider {
    border-right: 0;
    border-bottom: 1px solid #e6e8ec;
  }
}
</style>
