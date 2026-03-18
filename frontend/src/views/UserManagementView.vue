<template>
  <div class="page-card user-page">
    <div class="toolbar">
      <div>
        <h2 class="title">账号管理</h2>
        <p class="sub-title">管理员创建普通用户账号（默认密码可在创建时设置）</p>
      </div>
      <el-button class="create-btn" @click="dialogVisible = true">创建用户</el-button>
    </div>

    <el-table :data="users" border style="margin-top: 12px" class="user-table">
      <el-table-column prop="phone" label="手机号" />
      <el-table-column label="角色" width="120">
        <template #default="{ row }">
          <span class="role-pill" :class="row.role">{{ row.role }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" min-width="170" />
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
.user-page {
  max-width: 980px;
  margin: 0 auto;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.title {
  margin: 0;
  font-size: 24px;
  color: #111827;
}

.sub-title {
  margin: 6px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.create-btn {
  background: #0f172a;
  border-color: #0f172a;
  color: #fff;
  border-radius: 12px;
}

.role-pill {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid #d1d5db;
  font-size: 12px;
  line-height: 1.2;
}

.role-pill.admin,
.role-pill.super {
  background: #111827;
  color: #fff;
  border-color: #111827;
}

.role-pill.user {
  color: #4b5563;
  background: #f9fafb;
}

.user-table :deep(.el-table__header th) {
  background: #f3f4f6;
  color: #111827;
}

.user-table :deep(.el-table td),
.user-table :deep(.el-table th) {
  border-color: #e5e7eb;
}

@media (max-width: 900px) {
  .title {
    font-size: 24px;
  }

  .sub-title {
    font-size: 14px;
  }
}
</style>
