<template>
  <div class="page-card">
    <div class="toolbar">
      <h3>用户管理</h3>
      <el-button type="primary" @click="dialogVisible = true">创建用户</el-button>
    </div>

    <el-table :data="users" border style="margin-top: 12px">
      <el-table-column prop="phone" label="手机号" />
      <el-table-column prop="role" label="角色" width="120" />
      <el-table-column label="状态" width="120">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">{{ row.is_active ? '启用' : '停用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-switch :model-value="row.is_active" @change="(v) => changeStatus(row, v)" />
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="创建用户" width="460px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="手机号"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role" style="width: 100%">
            <el-option label="普通用户" value="user" />
            <el-option label="超级用户" value="super" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createUser">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { userApi } from '../api'

const users = ref([])
const dialogVisible = ref(false)
const form = reactive({ phone: '', password: '', role: 'user' })

async function loadData() {
  try {
    const resp = await userApi.list()
    users.value = resp.data.items
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '获取用户失败')
  }
}

async function createUser() {
  try {
    await userApi.create(form)
    ElMessage.success('创建成功')
    dialogVisible.value = false
    form.phone = ''
    form.password = ''
    form.role = 'user'
    loadData()
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '创建失败')
  }
}

async function changeStatus(row, value) {
  try {
    await userApi.updateStatus(row.id, { is_active: value })
    ElMessage.success('状态已更新')
    loadData()
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '状态更新失败')
  }
}

onMounted(loadData)
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
