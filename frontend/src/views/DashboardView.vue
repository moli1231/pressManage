<template>
  <div class="page-card">
    <h2 class="page-title">系统工作台</h2>
    <p class="page-subtitle">企业设备与有效期追踪平台</p>

    <div class="dashboard-grid">
      <div class="stat-card">
        <div class="stat-label">普通用户</div>
        <div class="stat-desc">查看压力表、修改密码</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">管理员</div>
        <div class="stat-desc">管理账号、查看提醒、导出数据</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">超级用户</div>
        <div class="stat-desc">压力表增删改、导入导出、上传图片</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-grid {
  margin-top: 16px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.stat-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  background: #f9fafb;
  padding: 14px;
}

.stat-label {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.stat-desc {
  margin-top: 6px;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.5;
}

@media (max-width: 900px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>
