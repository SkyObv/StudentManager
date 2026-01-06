<script>
export default {
  name: 'ApplyHostelCard',
  props: {
    hostelInfo: {
      type: Object,
      required: true
    }
  },
  methods : {
    apply_click(){ // 申请按钮点击
      let token = this.$settings.getToken()
      const hostel_id = this.hostelInfo.id
      console.log(`申请的宿舍id : ${hostel_id}`)
      console.log(`我的身份令牌为 ： ${token}`)
    },
  },
  computed: {
    genderText() { //获取性别显示文本映射
      return {
        'male': '男生宿舍',
        'female': '女生宿舍'
      };
    },

    genderIcon() {  // 获取性别图标映射
      return {
        'male': '♂',
        'female': '♀'
      };
    }
  }
}
</script>

<template>
  <div class="hostel-card">
    <!-- 卡片头部 -->
    <div class="card-header">
      <h3 class="hostel-number">{{ hostelInfo.hostel_number }}</h3>
    </div>
    
    <!-- 宿舍信息 -->
    <div class="hostel-info">
      <div class="info-row">
        <span class="info-label">楼层：</span>
        <span class="info-value">{{ hostelInfo.floor_name }}楼</span>
      </div>
      <div class="info-row">
        <span class="info-label">性别：</span>
        <span class="info-value gender-badge" :class="hostelInfo.gender">
          {{ genderIcon[hostelInfo.gender] }} {{ genderText[hostelInfo.gender] }}
        </span>
      </div>
      <div class="info-row">
        <span class="info-label">学生人数：</span>
        <span class="info-value">{{ hostelInfo.student_count }}人</span>
      </div>
      <div class="info-row">
        <span class="info-label">宿舍管理员：</span>
        <span class="info-value">
          <span v-if="hostelInfo.manager_name">{{ hostelInfo.manager_name }}</span>
          <span v-else class="no-manager">无</span>
        </span>
      </div>
      <div class="info-row">
        <span class="info-label">宿舍ID：</span>
        <span class="info-value">{{ hostelInfo.id }}</span>
      </div>
    </div>
    
    <!-- 操作按钮 -->
    <div class="card-actions" @click="apply_click">
      <button class="apply-manager-button">
        <span class="button-icon">👤</span>
        申请管理员
      </button>
    </div>
  </div>
</template>

<style scoped>
/* 宿舍卡片 */
.hostel-card {
  background: linear-gradient(135deg, #ffffff, #f8fafc);
  border-radius: 16px;
  padding: 25px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 380px;
}

.hostel-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
}

.hostel-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f1f5f9;
}

.hostel-number {
  font-size: 24px;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 宿舍信息 */
.hostel-info {
  margin-bottom: 25px;
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
  font-size: 15px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-label {
  color: #64748b;
  min-width: 80px;
  font-weight: 500;
  font-size: 14px;
}

.info-value {
  color: #1e293b;
  font-weight: 600;
}

.gender-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.gender-badge.male {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #1d4ed8;
  border: 1px solid #bfdbfe;
}

.gender-badge.female {
  background: linear-gradient(135deg, #fce7f3, #fbcfe8);
  color: #be185d;
  border: 1px solid #fbcfe8;
}

/* 无管理员样式 */
.no-manager {
  color: #9ca3af;
  font-style: italic;
}

/* 操作按钮 */
.card-actions {
  display: flex;
  justify-content: flex-end;
  padding: 20px 0 0 0;
  border-top: 1px solid #f1f5f9;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  margin-top: auto;
}

.button-icon {
  font-size: 14px;
}

/* 管理员操作按钮样式 */
.apply-manager-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  line-height: 20px;
  min-height: 40px;
  background-color: #10b981;
  color: white;
}

.apply-manager-button:hover {
  background-color: #059669;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}
</style>