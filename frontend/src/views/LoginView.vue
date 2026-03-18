<template>
  <div class="login-wrap">
    <div class="login-card">
      <h1>压力表管理系统</h1>
      <p class="desc">企业设备与有效期追踪平台</p>
      <p class="hint">演示账号：超管 13800000000 / Admin@123，管理员 13900000000 / Admin@123，普通用户 13700000000 / User@123</p>
      <el-form :model="form" @submit.prevent="onSubmit">
        <el-form-item>
          <el-input v-model="form.phone" placeholder="手机号" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" show-password />
        </el-form-item>
        <el-button type="primary" style="width: 100%" :loading="loading" @click="onSubmit">登录</el-button>
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
  padding: 30px;
  border-radius: 14px;
  background: #fff;
  border: 1px solid #e5e7eb;
  box-shadow: 0 4px 16px rgba(17, 24, 39, 0.06);
}

h1 {
  margin: 0;
  color: #111827;
  font-size: 24px;
}

.desc {
  margin: 8px 0 18px;
  color: #6b7280;
  font-size: 14px;
}

.hint {
  margin: 0 0 18px;
  font-size: 12px;
  line-height: 1.5;
  color: #6b7280;
}
</style>
