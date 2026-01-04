<script>
export default {
  name: 'ApplyHostelCard',
  props: {
    hostelInfo: {
      type: Object,
      required: true
    }
  },
  computed: {
    /**
     * 获取性别显示文本映射
     */
    genderText() {
      return {
        'male': '男生宿舍',
        'female': '女生宿舍'
      };
    },
    
    /**
     * 获取性别图标映射
     */
    genderIcon() {
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
      <div class="room-info">
        <h3 class="room-number">{{ hostelInfo.hostel_number }}</h3>
        <span class="floor-badge">{{ hostelInfo.floor_name }}楼</span>
      </div>
      <div :class="['gender-indicator', hostelInfo.gender]">
        <span class="gender-icon">{{ genderIcon[hostelInfo.gender] }}</span>
        <span class="gender-text">{{ genderText[hostelInfo.gender] }}</span>
      </div>
    </div>
    
    <!-- 卡片内容 -->
    <div class="card-content">
      <div class="info-section">
        <div class="info-item">
          <span class="info-label">宿舍ID</span>
          <span class="info-value">{{ hostelInfo.id }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">管理员</span>
          <span class="info-value">
            <span v-if="hostelInfo.manager_name">{{ hostelInfo.manager_name }}</span>
            <span v-else class="no-manager">暂缺</span>
          </span>
        </div>
      </div>
    </div>
    
    <!-- 卡片底部 -->
    <div class="card-footer">
      <button class="apply-manager-btn">
        申请管理员
      </button>
    </div>
  </div>
</template>

<style scoped>
/* 宿舍卡片 */
.hostel-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  min-height: 220px;
}

.hostel-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
  border-color: #d1d5db;
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f3f4f6;
}

.room-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.room-number {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin: 0;
}

.floor-badge {
  display: inline-block;
  padding: 4px 10px;
  background: #f3f4f6;
  color: #6b7280;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.gender-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 500;
}

.gender-indicator.male {
  background: #dbeafe;
  color: #1e40af;
}

.gender-indicator.female {
  background: #fce7f3;
  color: #be185d;
}

.gender-icon {
  font-size: 16px;
}

.gender-text {
  font-size: 12px;
}

/* 卡片内容 */
.card-content {
  flex: 1;
  margin-bottom: 16px;
}

.info-section {
  background: #f9fafb;
  padding: 14px;
  border-radius: 8px;
  border: 1px solid #f3f4f6;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 14px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-label {
  color: #6b7280;
  font-weight: 500;
}

.info-value {
  color: #111827;
  font-weight: 600;
}

.no-manager {
  color: #9ca3af;
  font-style: normal;
}

/* 卡片底部 */
.card-footer {
  display: flex;
  justify-content: center;
}

.apply-manager-btn {
  width: 100%;
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.25);
}

.apply-manager-btn:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.35);
  transform: translateY(-1px);
}

.apply-manager-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.25);
}
</style>