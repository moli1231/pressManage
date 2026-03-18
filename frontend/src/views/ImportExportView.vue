<template>
  <div class="page-card">
    <h2 class="page-title">Excel 导入导出</h2>
    <p class="page-subtitle">管理员可导出，超级用户可导入与导出</p>

    <div class="page-toolbar">
      <div class="toolbar-actions">
        <template v-if="isSuper">
          <input type="file" accept=".xlsx" @change="onFileChange" />
          <el-button class="dark-btn" :disabled="!file" @click="importExcel">导入</el-button>
        </template>
      </div>
      <div class="toolbar-actions">
        <el-button @click="exportExcel">导出</el-button>
      </div>
    </div>

    <el-alert
      v-if="result"
      style="margin-top: 12px"
      type="info"
      :title="`导入成功 ${result.success} 条，失败 ${result.errors.length} 条`"
      show-icon
      :closable="false"
    />

    <el-table v-if="result?.errors?.length" :data="result.errors" border style="margin-top: 12px" class="panel-table">
      <el-table-column prop="row" label="行号" width="100" />
      <el-table-column prop="error" label="错误原因" />
    </el-table>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { gaugeApi } from '../api'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const isSuper = computed(() => auth.role === 'super')
const file = ref(null)
const result = ref(null)

function onFileChange(event) {
  file.value = event.target.files?.[0] || null
}

async function importExcel() {
  if (!isSuper.value) {
    ElMessage.warning('仅超级用户可导入')
    return
  }
  if (!file.value) return
  const formData = new FormData()
  formData.append('file', file.value)
  try {
    const resp = await gaugeApi.importExcel(formData)
    result.value = resp.data
    ElMessage.success('导入完成')
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '导入失败')
  }
}

function exportExcel() {
  gaugeApi
    .exportExcel()
    .then((resp) => {
      const url = URL.createObjectURL(resp.data.blob)
      const a = document.createElement('a')
      a.href = url
      a.download = resp.data.filename || 'gauges.csv'
      a.click()
      URL.revokeObjectURL(url)
      ElMessage.success('导出成功')
    })
    .catch((e) => {
      ElMessage.error(e?.response?.data?.message || e.message || '导出失败')
    })
}
</script>
