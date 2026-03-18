<template>
  <div class="login-wrap">
    <div class="login-card">
      <div class="card-head">
        <div class="brand-row">
          <div class="brand-logo" aria-hidden="true">
            <svg viewBox="0 0 64 64" class="logo-svg">
              <circle cx="32" cy="32" r="26" fill="#0f172a" />
              <circle cx="32" cy="32" r="17" fill="none" stroke="#f8fafc" stroke-width="3.5" />
              <path d="M32 32 L44 24" stroke="#f8fafc" stroke-width="3.5" stroke-linecap="round" />
              <circle cx="32" cy="32" r="2.8" fill="#f8fafc" />
              <path d="M20 47h24" stroke="#f8fafc" stroke-width="3" stroke-linecap="round" />
            </svg>
          </div>
          <h1>采气二厂工艺设备管理系统</h1>
        </div>
        <p class="desc">企业设备与有效期追踪平台</p>
      </div>
      <el-form :model="form" @submit.prevent="onSubmit">
        <el-form-item>
          <el-input v-model="form.phone" placeholder="手机号">
            <template #prefix>
              <span class="input-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24">
                  <path d="M6.6 2.5h2.8c.5 0 .9.3 1 .8l.8 3.3c.1.4 0 .9-.4 1.2L8.9 9.3a13.3 13.3 0 0 0 5.8 5.8l1.5-1.9c.3-.4.8-.5 1.2-.4l3.3.8c.5.1.8.5.8 1v2.8c0 .6-.5 1.1-1.1 1.1C10.7 21.5 2.5 13.3 2.5 3.6c0-.6.5-1.1 1.1-1.1Z" fill="currentColor" />
                </svg>
              </span>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" show-password>
            <template #prefix>
              <span class="input-icon" aria-hidden="true">
                <svg viewBox="0 0 24 24">
                  <path d="M7 10V8a5 5 0 0 1 10 0v2h1.5c.8 0 1.5.7 1.5 1.5v8c0 .8-.7 1.5-1.5 1.5h-13c-.8 0-1.5-.7-1.5-1.5v-8C4 10.7 4.7 10 5.5 10H7Zm2 0h6V8a3 3 0 0 0-6 0v2Zm3 3a2 2 0 0 1 1 3.7V18h-2v-1.3A2 2 0 0 1 12 13Z" fill="currentColor" />
                </svg>
              </span>
            </template>
          </el-input>
        </el-form-item>
        <el-button class="dark-btn login-btn" :loading="loading" @click="onSubmit">登录</el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { authApi } from '../api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const store = useAuthStore()
const loading = ref(false)
const form = reactive({ phone: '13800000000', password: 'Admin@123' })

async function onSubmit() {
  if (!form.phone || !form.password) {
    ElMessage.warning('请填写手机号和密码')
    return
  }
  loading.value = true
  try {
    const resp = await authApi.login(form)
    store.setAuth(resp.data.token, resp.data.user)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: #f3f4f6;
}

.login-card {
  width: 460px;
  max-width: 100%;
  padding: 0;
  border-radius: 14px;
  background: #fff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 16px rgba(17, 24, 39, 0.06);
  overflow: hidden;
}

.card-head {
  padding: 24px 28px 16px;
  border-bottom: 1px solid #eceff3;
  background: #f7f8fa;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-logo {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  flex: 0 0 auto;
}

.logo-svg {
  width: 34px;
  height: 34px;
}

h1 {
  margin: 0;
  color: #111827;
  font-size: 20px;
}

.desc {
  margin: 8px 0 18px;
  color: #6b7280;
  font-size: 14px;
}

:deep(.el-form) {
  padding: 18px 28px 28px;
}

.login-btn {
  width: 100%;
}

.input-icon {
  width: 16px;
  height: 16px;
  color: #6b7280;
  display: inline-flex;
}

.input-icon svg {
  width: 16px;
  height: 16px;
}
</style>
