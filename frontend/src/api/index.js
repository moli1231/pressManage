const STORAGE_KEY = 'pgms_mock_db_v1'

function addDays(dateText, days) {
  const date = new Date(dateText)
  date.setDate(date.getDate() + Number(days))
  return date.toISOString().slice(0, 10)
}

function daysLeft(validUntil) {
  const now = new Date()
  now.setHours(0, 0, 0, 0)
  const due = new Date(validUntil)
  due.setHours(0, 0, 0, 0)
  return Math.floor((due.getTime() - now.getTime()) / 86400000)
}

function expiryStatus(remainingDays) {
  if (remainingDays < 0) return 'expired'
  if (remainingDays === 0) return 'expires_today'
  return 'active'
}

function seedDb() {
  const gauges = [
    {
      id: 1,
      gauge_code: 'PG-2026-0001',
      inspection_days: 365,
      manufacturer: '华东仪表',
      serial_no: 'SN-E10001',
      location: 'A厂-锅炉房1',
      entity_photo_path: '',
      report_photo_path: '',
      calibration_date: '2025-04-17',
      gauge_type: 'electronic',
      created_by: 1,
      reminded_30: false,
      reminded_15: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: 2,
      gauge_code: 'PG-2026-0002',
      inspection_days: 180,
      manufacturer: '北方机械',
      serial_no: 'SN-M20002',
      location: 'B厂-储罐区',
      entity_photo_path: '',
      report_photo_path: '',
      calibration_date: '2025-10-20',
      gauge_type: 'mechanical',
      created_by: 1,
      reminded_30: false,
      reminded_15: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
    {
      id: 3,
      gauge_code: 'PG-2026-0003',
      inspection_days: 90,
      manufacturer: '精工电子',
      serial_no: 'SN-E30003',
      location: 'C厂-压缩机房',
      entity_photo_path: '',
      report_photo_path: '',
      calibration_date: '2025-12-28',
      gauge_type: 'electronic',
      created_by: 2,
      reminded_30: false,
      reminded_15: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    },
  ].map((item) => ({ ...item, valid_until: addDays(item.calibration_date, item.inspection_days) }))

  return {
    users: [
      { id: 1, phone: '13800000000', password: 'Admin@123', role: 'super', is_active: true, created_at: new Date().toISOString() },
      { id: 2, phone: '13900000000', password: 'Admin@123', role: 'admin', is_active: true, created_at: new Date().toISOString() },
      { id: 3, phone: '13700000000', password: 'User@123', role: 'user', is_active: true, created_at: new Date().toISOString() },
    ],
    gauges,
    reminders: [],
    nextUserId: 4,
    nextGaugeId: 4,
    nextReminderId: 1,
  }
}

function loadDb() {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) {
    const data = seedDb()
    saveDb(data)
    return data
  }
  return JSON.parse(raw)
}

function saveDb(db) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(db))
}

function ok(data = {}, message = 'ok') {
  return Promise.resolve({ code: 0, message, data })
}

function fail(message) {
  return Promise.reject(new Error(message))
}

function getCurrentUser() {
  const raw = localStorage.getItem('user')
  if (!raw) return null
  return JSON.parse(raw)
}

function requireRoles(roles) {
  const user = getCurrentUser()
  if (!user) throw new Error('请先登录')
  if (!roles.includes(user.role)) throw new Error('无权限访问')
  return user
}

function toSafeUser(user) {
  return {
    id: user.id,
    phone: user.phone,
    role: user.role,
    is_active: user.is_active,
    created_at: user.created_at,
  }
}

function hydrateGauge(item) {
  const remaining_days = daysLeft(item.valid_until)
  return {
    ...item,
    remaining_days,
    expiry_status: expiryStatus(remaining_days),
  }
}

function runReminderScanInternal(db) {
  const currentUser = getCurrentUser()
  const created = []
  db.gauges.forEach((gauge) => {
    const remaining = daysLeft(gauge.valid_until)
    if (remaining === 30 && !gauge.reminded_30) {
      gauge.reminded_30 = true
      const item = {
        id: db.nextReminderId++,
        gauge_id: gauge.id,
        reminder_type: '30_days',
        sent_at: new Date().toISOString(),
        sent_by: currentUser?.id || null,
      }
      db.reminders.push(item)
      created.push(item)
    }
    if (remaining === 15 && !gauge.reminded_15) {
      gauge.reminded_15 = true
      const item = {
        id: db.nextReminderId++,
        gauge_id: gauge.id,
        reminder_type: '15_days',
        sent_at: new Date().toISOString(),
        sent_by: currentUser?.id || null,
      }
      db.reminders.push(item)
      created.push(item)
    }
  })
  return created
}

function readFileAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = () => reject(new Error('读取文件失败'))
    reader.readAsDataURL(file)
  })
}

export const authApi = {
  async login(payload) {
    const db = loadDb()
    const phone = String(payload?.phone || '').trim()
    const password = String(payload?.password || '').trim()
    if (!phone || !password) return fail('手机号和密码必填')

    const user = db.users.find((item) => item.phone === phone)
    if (!user || user.password !== password) return fail('手机号或密码错误')
    if (!user.is_active) return fail('账号已禁用')

    return ok({ token: `mock-${user.id}-${Date.now()}`, user: toSafeUser(user) }, '登录成功')
  },

  async changePassword(payload) {
    const current = requireRoles(['user', 'admin', 'super'])
    const db = loadDb()
    const user = db.users.find((item) => item.id === current.id)
    const oldPassword = String(payload?.old_password || '')
    const newPassword = String(payload?.new_password || '')

    if (!user || user.password !== oldPassword) return fail('旧密码错误')
    if (newPassword.length < 6) return fail('新密码至少 6 位')

    user.password = newPassword
    saveDb(db)
    return ok({}, '密码修改成功')
  },
}

export const userApi = {
  async create(payload) {
    requireRoles(['admin', 'super'])
    const db = loadDb()
    const phone = String(payload?.phone || '').trim()
    const password = String(payload?.password || '').trim()
    const role = String(payload?.role || 'user').trim()

    if (!phone || !password) return fail('手机号和密码必填')
    if (!['user', 'super'].includes(role)) return fail('只能创建普通用户或超级用户')
    if (db.users.some((item) => item.phone === phone)) return fail('手机号已存在')

    const user = {
      id: db.nextUserId++,
      phone,
      password,
      role,
      is_active: true,
      created_at: new Date().toISOString(),
    }
    db.users.unshift(user)
    saveDb(db)
    return ok(toSafeUser(user), '创建成功')
  },

  async list() {
    requireRoles(['admin', 'super'])
    const db = loadDb()
    return ok({ items: db.users.map(toSafeUser), total: db.users.length })
  },

  async updateStatus(id, payload) {
    requireRoles(['admin', 'super'])
    const db = loadDb()
    const user = db.users.find((item) => item.id === Number(id))
    if (!user) return fail('用户不存在')

    user.is_active = Boolean(payload?.is_active)
    saveDb(db)
    return ok(toSafeUser(user), '状态更新成功')
  },
}

export const gaugeApi = {
  async list(params = {}) {
    requireRoles(['user', 'admin', 'super'])
    const db = loadDb()
    const page = Number(params.page || 1)
    const page_size = Number(params.page_size || 10)
    const keyword = String(params.keyword || '').trim()

    let items = db.gauges
    if (keyword) {
      items = items.filter((item) => item.gauge_code.includes(keyword))
    }
    items = items.slice().sort((a, b) => new Date(b.created_at) - new Date(a.created_at))

    const total = items.length
    const start = (page - 1) * page_size
    const pageItems = items.slice(start, start + page_size).map(hydrateGauge)

    return ok({ items: pageItems, total, page, page_size })
  },

  async detail(id) {
    requireRoles(['user', 'admin', 'super'])
    const db = loadDb()
    const item = db.gauges.find((gauge) => gauge.id === Number(id))
    if (!item) return fail('记录不存在')
    return ok(hydrateGauge(item))
  },

  async create(payload) {
    const current = requireRoles(['super'])
    const db = loadDb()
    const gauge_code = String(payload?.gauge_code || '').trim()
    const calibration_date = String(payload?.calibration_date || '').trim()
    const inspection_days = Number(payload?.inspection_days)

    if (!gauge_code || !calibration_date || !inspection_days) return fail('请填写必填字段')
    if (!['electronic', 'mechanical'].includes(payload?.gauge_type)) return fail('压力表类型无效')
    if (db.gauges.some((item) => item.gauge_code === gauge_code)) return fail('压力表编号已存在')

    const item = {
      id: db.nextGaugeId++,
      gauge_code,
      inspection_days,
      manufacturer: String(payload?.manufacturer || '').trim(),
      serial_no: String(payload?.serial_no || '').trim(),
      location: String(payload?.location || '').trim(),
      entity_photo_path: payload?.entity_photo_path || '',
      report_photo_path: payload?.report_photo_path || '',
      calibration_date,
      valid_until: addDays(calibration_date, inspection_days),
      gauge_type: payload?.gauge_type,
      created_by: current.id,
      reminded_30: false,
      reminded_15: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }

    db.gauges.unshift(item)
    saveDb(db)
    return ok(hydrateGauge(item), '创建成功')
  },

  async update(id, payload) {
    requireRoles(['super'])
    const db = loadDb()
    const item = db.gauges.find((gauge) => gauge.id === Number(id))
    if (!item) return fail('记录不存在')

    const nextCode = String(payload?.gauge_code || item.gauge_code).trim()
    const exists = db.gauges.find((gauge) => gauge.gauge_code === nextCode && gauge.id !== item.id)
    if (exists) return fail('压力表编号已存在')

    item.gauge_code = nextCode
    item.inspection_days = Number(payload?.inspection_days ?? item.inspection_days)
    item.manufacturer = String(payload?.manufacturer ?? item.manufacturer)
    item.serial_no = String(payload?.serial_no ?? item.serial_no)
    item.location = String(payload?.location ?? item.location)
    item.entity_photo_path = payload?.entity_photo_path ?? item.entity_photo_path
    item.report_photo_path = payload?.report_photo_path ?? item.report_photo_path
    item.calibration_date = String(payload?.calibration_date || item.calibration_date)
    item.gauge_type = payload?.gauge_type || item.gauge_type
    item.valid_until = addDays(item.calibration_date, item.inspection_days)
    item.reminded_30 = false
    item.reminded_15 = false
    item.updated_at = new Date().toISOString()

    saveDb(db)
    return ok(hydrateGauge(item), '更新成功')
  },

  async remove(id) {
    requireRoles(['super'])
    const db = loadDb()
    db.gauges = db.gauges.filter((item) => item.id !== Number(id))
    saveDb(db)
    return ok({}, '删除成功')
  },

  async importExcel(formData) {
    const current = requireRoles(['super'])
    const db = loadDb()
    const file = formData.get('file')
    if (!file) return fail('请上传文件')

    const now = new Date().toISOString().slice(0, 10)
    const code = `PG-IMPORT-${Date.now().toString().slice(-6)}`
    const item = {
      id: db.nextGaugeId++,
      gauge_code: code,
      inspection_days: 365,
      manufacturer: '批量导入(模拟)',
      serial_no: `AUTO-${db.nextGaugeId}`,
      location: '待确认位置',
      entity_photo_path: '',
      report_photo_path: '',
      calibration_date: now,
      valid_until: addDays(now, 365),
      gauge_type: 'electronic',
      created_by: current.id,
      reminded_30: false,
      reminded_15: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }
    db.gauges.unshift(item)
    saveDb(db)

    return ok({ success: 1, errors: [], note: '当前为前端独立模式，导入为模拟写入 1 条记录。' }, '导入完成')
  },

  async exportExcel() {
    requireRoles(['admin', 'super'])
    const db = loadDb()
    const header = ['压力表编号', '检测时间(天)', '厂商', '编号', '放置位置', '校准日期', '有效期', '类型']
    const rows = db.gauges.map((item) => [
      item.gauge_code,
      item.inspection_days,
      item.manufacturer,
      item.serial_no,
      item.location,
      item.calibration_date,
      item.valid_until,
      item.gauge_type === 'electronic' ? '电子表' : '机械表',
    ])
    const csv = [header, ...rows]
      .map((row) => row.map((cell) => `"${String(cell ?? '').replaceAll('"', '""')}"`).join(','))
      .join('\n')

    const blob = new Blob([`\ufeff${csv}`], { type: 'text/csv;charset=utf-8;' })
    const filename = `gauges-${new Date().toISOString().slice(0, 10)}.csv`
    return ok({ blob, filename }, '导出完成')
  },
}

export const fileApi = {
  async upload(formData) {
    requireRoles(['super'])
    const file = formData.get('file')
    if (!file) return fail('文件不能为空')
    const path = await readFileAsDataUrl(file)
    return ok({ path, filename: file.name || 'upload-image' }, '上传成功')
  },
}

export const reminderApi = {
  async list() {
    requireRoles(['admin', 'super'])
    const db = loadDb()
    const items = db.reminders.slice().sort((a, b) => new Date(b.sent_at) - new Date(a.sent_at))
    return ok({ items, total: items.length })
  },

  async run() {
    requireRoles(['admin', 'super'])
    const db = loadDb()
    const created = runReminderScanInternal(db)
    saveDb(db)
    return ok({ created, count: created.length }, '执行完成')
  },
}
