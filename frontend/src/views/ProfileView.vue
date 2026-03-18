<template>
  <div class="page-card profile-card">
    <h2 class="page-title">修改密码</h2>
    <p class="page-subtitle">为保障账号安全，请定期更换密码</p>

    <el-form :model="form" label-width="100px" class="profile-form">
      <el-form-item label="旧密码"><el-input v-model="form.old_password" type="password" show-password /></el-form-item>
      <el-form-item label="新密码"><el-input v-model="form.new_password" type="password" show-password /></el-form-item>
      <el-button class="dark-btn" @click="changePassword">保存</el-button>
    </el-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { authApi } from '../api'

const form = reactive({ old_password: '', new_password: '' })

async function changePassword() {
  try {
    await authApi.changePassword(form)
    ElMessage.success('密码修改成功')
    form.old_password = ''
    form.new_password = ''
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '修改失败')
  }
}
</script>

<style scoped>
.profile-card {
  max-width: 640px;
}

.profile-form {
  max-width: 460px;
  margin-top: 14px;
}
</style>
