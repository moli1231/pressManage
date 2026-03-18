<template>
  <div class="page-card">
    <h2 class="page-title">到期提醒</h2>
    <p class="page-subtitle">系统记录 30 天和 15 天的提醒触发结果</p>

    <div class="page-toolbar">
      <div />
      <div class="toolbar-actions">
        <el-button class="dark-btn" @click="runNow">立即扫描提醒</el-button>
      </div>
    </div>

    <el-table :data="items" border style="margin-top: 12px" class="panel-table">
      <el-table-column prop="gauge_id" label="压力表ID" width="120" />
      <el-table-column prop="reminder_type" label="提醒类型" width="140" />
      <el-table-column prop="sent_at" label="提醒时间" />
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { reminderApi } from '../api'

const items = ref([])

async function loadData() {
  try {
    const resp = await reminderApi.list()
    items.value = resp.data.items
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '获取提醒失败')
  }
}

async function runNow() {
  try {
    const resp = await reminderApi.run()
    ElMessage.success(`本次新增 ${resp.data.count} 条提醒`)
    loadData()
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '执行失败')
  }
}

onMounted(loadData)
</script>
