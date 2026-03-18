<template>
  <div class="page-card">
    <h2 class="page-title">压力表列表</h2>
    <p class="page-subtitle">支持查询、新增、编辑、删除与图片管理</p>

    <div class="page-toolbar">
      <el-input v-model="query.keyword" placeholder="按压力表编号搜索" class="search-input" @keyup.enter="loadData" />
      <div class="toolbar-actions">
        <el-button @click="loadData">查询</el-button>
        <el-button v-if="isSuper" class="dark-btn" @click="openCreate">新增压力表</el-button>
      </div>
    </div>

    <el-table :data="list" border style="width: 100%; margin-top: 14px" class="panel-table">
      <el-table-column prop="gauge_code" label="压力表编号" width="150" />
      <el-table-column prop="manufacturer" label="厂商" width="140" />
      <el-table-column prop="serial_no" label="编号" width="140" />
      <el-table-column prop="location" label="放置位置" min-width="160" />
      <el-table-column prop="gauge_type" label="类型" width="120">
        <template #default="{ row }">{{ typeLabel(row.gauge_type) }}</template>
      </el-table-column>
      <el-table-column label="实体照片" width="100">
        <template #default="{ row }">
          <el-image
            v-if="row.entity_photo_path"
            style="width: 44px; height: 44px; border-radius: 6px"
            :src="toFileUrl(row.entity_photo_path)"
            fit="cover"
            :preview-src-list="[toFileUrl(row.entity_photo_path)]"
            preview-teleported
          />
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column label="检测报告" width="100">
        <template #default="{ row }">
          <el-image
            v-if="row.report_photo_path"
            style="width: 44px; height: 44px; border-radius: 6px"
            :src="toFileUrl(row.report_photo_path)"
            fit="cover"
            :preview-src-list="[toFileUrl(row.report_photo_path)]"
            preview-teleported
          />
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column label="校准日期" width="120">
        <template #default="{ row }">{{ row.calibration_date || '-' }}</template>
      </el-table-column>
      <el-table-column label="有效期" width="120">
        <template #default="{ row }">{{ row.valid_until || '-' }}</template>
      </el-table-column>
      <el-table-column label="剩余天数" width="120">
        <template #default="{ row }">
          <el-tag :type="remainingTagType(row.remaining_days)">{{ renderRemaining(row.remaining_days) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right" v-if="isSuper">
        <template #default="{ row }">
          <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="removeItem(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      style="margin-top: 14px"
      background
      layout="total, prev, pager, next"
      :total="total"
      :current-page="query.page"
      :page-size="query.page_size"
      @current-change="(p) => { query.page = p; loadData() }"
    />

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑压力表' : '新增压力表'" width="700px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="压力表编号"><el-input v-model="form.gauge_code" /></el-form-item>
        <el-form-item label="检测时间(天)"><el-input-number v-model="form.inspection_days" :min="1" /></el-form-item>
        <el-form-item label="厂商"><el-input v-model="form.manufacturer" /></el-form-item>
        <el-form-item label="编号"><el-input v-model="form.serial_no" /></el-form-item>
        <el-form-item label="放置位置"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="校准日期"><el-date-picker value-format="YYYY-MM-DD" v-model="form.calibration_date" /></el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.gauge_type" style="width: 100%">
            <el-option label="电子表" value="electronic" />
            <el-option label="机械表" value="mechanical" />
          </el-select>
        </el-form-item>
        <el-form-item label="实体照片">
          <div class="upload-row">
            <input type="file" accept=".jpg,.jpeg,.png,.webp" @change="(e) => onUpload(e, 'entity_photo_path')" />
            <el-image
              v-if="form.entity_photo_path"
              class="upload-preview"
              :src="toFileUrl(form.entity_photo_path)"
              fit="cover"
              :preview-src-list="[toFileUrl(form.entity_photo_path)]"
              preview-teleported
            />
          </div>
        </el-form-item>
        <el-form-item label="检测报告照片">
          <div class="upload-row">
            <input type="file" accept=".jpg,.jpeg,.png,.webp" @change="(e) => onUpload(e, 'report_photo_path')" />
            <el-image
              v-if="form.report_photo_path"
              class="upload-preview"
              :src="toFileUrl(form.report_photo_path)"
              fit="cover"
              :preview-src-list="[toFileUrl(form.report_photo_path)]"
              preview-teleported
            />
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button class="dark-btn" :loading="saving" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { fileApi, gaugeApi } from '../api'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const isSuper = computed(() => auth.role === 'super')

const list = ref([])
const total = ref(0)
const dialogVisible = ref(false)
const saving = ref(false)
const query = reactive({ page: 1, page_size: 10, keyword: '' })
const form = reactive({
  id: null,
  gauge_code: '',
  inspection_days: 365,
  manufacturer: '',
  serial_no: '',
  location: '',
  calibration_date: '',
  gauge_type: 'electronic',
  entity_photo_path: '',
  report_photo_path: '',
})

function resetForm() {
  Object.assign(form, {
    id: null,
    gauge_code: '',
    inspection_days: 365,
    manufacturer: '',
    serial_no: '',
    location: '',
    calibration_date: '',
    gauge_type: 'electronic',
    entity_photo_path: '',
    report_photo_path: '',
  })
}

function renderRemaining(days) {
  if (typeof days !== 'number') return '-'
  return days < 0 ? '已过期' : `${days} 天`
}

function remainingTagType(days) {
  if (typeof days !== 'number') return 'info'
  if (days < 0) return 'danger'
  if (days <= 30) return 'warning'
  return 'success'
}

function typeLabel(type) {
  return type === 'electronic' ? '电子表' : type === 'mechanical' ? '机械表' : type || '-'
}

function toFileUrl(path) {
  if (!path) return ''
  return path.startsWith('http') ? path : `/api/v1${path}`
}

async function onUpload(event, field) {
  const targetFile = event.target.files?.[0]
  if (!targetFile) return
  const formData = new FormData()
  formData.append('file', targetFile)
  try {
    const resp = await fileApi.upload(formData)
    form[field] = resp.data.path
    ElMessage.success('上传成功')
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '上传失败')
  } finally {
    event.target.value = ''
  }
}

async function loadData() {
  try {
    const resp = await gaugeApi.list(query)
    list.value = resp.data.items
    total.value = resp.data.total
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '获取列表失败')
  }
}

function openCreate() {
  resetForm()
  dialogVisible.value = true
}

function openEdit(row) {
  Object.assign(form, {
    id: row.id,
    gauge_code: row.gauge_code,
    inspection_days: row.inspection_days,
    manufacturer: row.manufacturer,
    serial_no: row.serial_no,
    location: row.location,
    calibration_date: row.calibration_date,
    gauge_type: row.gauge_type,
    entity_photo_path: row.entity_photo_path || '',
    report_photo_path: row.report_photo_path || '',
  })
  dialogVisible.value = true
}

function buildPayload() {
  return {
    gauge_code: form.gauge_code,
    inspection_days: form.inspection_days,
    manufacturer: form.manufacturer,
    serial_no: form.serial_no,
    location: form.location,
    calibration_date: form.calibration_date,
    gauge_type: form.gauge_type,
    entity_photo_path: form.entity_photo_path || null,
    report_photo_path: form.report_photo_path || null,
  }
}

async function submit() {
  saving.value = true
  try {
    const payload = buildPayload()
    if (form.id) {
      await gaugeApi.update(form.id, payload)
    } else {
      await gaugeApi.create(payload)
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error(e?.response?.data?.message || e.message || '保存失败')
  } finally {
    saving.value = false
  }
}

async function removeItem(row) {
  try {
    await ElMessageBox.confirm(`确认删除 ${row.gauge_code} 吗？`, '提示')
    await gaugeApi.remove(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (_) {
    // 用户取消不提示
  }
}

onMounted(loadData)
</script>

<style scoped>
.search-input {
  width: 280px;
}

.upload-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.upload-preview {
  width: 56px;
  height: 56px;
  border-radius: 6px;
}

@media (max-width: 900px) {
  .search-input {
    width: 100%;
  }
}
</style>
