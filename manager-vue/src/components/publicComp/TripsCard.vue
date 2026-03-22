<script>
export default {
  name: 'TripsCard',
  props: {
            //  {
            //   "id": 1,
            //   "number": "21321321321",
            //   "manager_teacher": {
            //       "id": 2,
            //       "name": "光头强",
            //       "user_type": "teacher",
            //       "is_active": true
            //   },
            //   "in_hostel": false,
            //   "update_time": "2026-03-22T10:09:21.328268+08:00",
            //   "create_time": "2026-03-22T10:09:21.328301+08:00",
            //   "key_card_state": true,
            //   "student": null
            // },
    keyCard: {
      type: Object,
      default: () => ({})
    }
  },
  computed: {
    cardStateClass() {
      return this.keyCard.key_card_state ? 'state-active' : 'state-inactive';
    },
    cardStateText() {
      return this.keyCard.key_card_state ? '激活' : '未激活';
    },
    inHostelText() {
      return this.keyCard.in_hostel ? '在宿舍' : '不在宿舍';
    },
    inHostelClass() {
      return this.keyCard.in_hostel ? 'in-hostel' : 'not-in-hostel';
    }
  },
  methods: {
    formatDateTime(timeStr) {
      if (!timeStr) return '';
      const date = new Date(timeStr);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    }
  }
}
</script>

<template>
  <div class="trips-card">
    <div class="card-header">
      <div class="header-content">
        <h3 class="card-number">门禁卡 {{ keyCard.number }}</h3>
        <div class="card-state" :class="cardStateClass">
          {{ cardStateText }}
        </div>
      </div>
      <div class="card-location" :class="inHostelClass">
        {{ inHostelText }}
      </div>
    </div>
    
    <div class="card-body">
      <div class="card-content">
        <div class="info-item">
          <span class="info-label">门禁卡号：</span>
          <span class="info-value">{{ keyCard.number }}</span>
        </div>
        
        <div class="info-item">
          <span class="info-label">管理教师：</span>
          <span class="info-value teacher-name">{{ keyCard.manager_teacher.name }}</span>
        </div>
        
        <div class="info-item">
          <span class="info-label">教师状态：</span>
          <span class="info-value" :class="keyCard.manager_teacher.is_active ? 'teacher-active' : 'teacher-inactive'">
            {{ keyCard.manager_teacher.is_active ? '在职' : '离职' }}
          </span>
        </div>
        
        <div class="info-item">
          <span class="info-label">所在位置：</span>
          <span class="info-value" :class="inHostelClass">
            {{ inHostelText }}
          </span>
        </div>
        
        <div class="info-item">
          <span class="info-label">绑定学生：</span>
          <span class="info-value">
            <span v-if="keyCard.student">{{ keyCard.student.name }}</span>
            <span v-else class="no-student">未绑定</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trips-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 16px 20px;
  margin: 0 8px 16px;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.5);
  position: relative;
  overflow: hidden;
  width: calc(33.333% - 16px);
  flex: 0 0 calc(33.333% - 16px);
  max-width: 384px;
}

.trips-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
}

.trips-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
  gap: 8px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-grow: 1;
  overflow: hidden;
}

.card-number {
  font-size: 22px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 1;
}

.card-state {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease;
  white-space: nowrap;
  z-index: 5;
}

.card-state:hover {
  transform: translateY(-1px);
}

.state-active {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  color: #155724;
  border: 1px solid #c3e6cb;
}

.state-inactive {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.card-location {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease;
  text-align: center;
  white-space: nowrap;
}

.in-hostel {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.not-in-hostel {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border: 1px solid #fde68a;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.6);
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid rgba(0, 0, 0, 0.03);
  transition: background 0.2s ease, border-color 0.2s ease;
  min-width: 120px;
  flex: 1;
}

.info-item:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(59, 130, 246, 0.2);
}

.info-label {
  font-size: 12px;
  color: #718096;
  font-weight: 500;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 4px;
}

.info-label::before {
  content: '•';
  color: #3b82f6;
  font-weight: bold;
  font-size: 16px;
}

.info-value {
  font-size: 13px;
  color: #2d3748;
  font-weight: 600;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.teacher-name {
  color: #3b82f6;
  font-weight: 700;
}

.teacher-active {
  color: #10b981;
}

.teacher-inactive {
  color: #ef4444;
}

.no-student {
  color: #9ca3af;
  font-style: italic;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.trips-card {
  animation: fadeInUp 0.3s ease-out;
}

@media (max-width: 768px) {
  .trips-card {
    padding: 20px 24px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 20px;
  }
  
  .header-content {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .card-number {
    font-size: 20px;
  }
  
  .card-content {
    flex-direction: column;
    gap: 12px;
  }
  
  .info-item {
    min-width: 100%;
    padding: 10px 16px;
  }
}

@media (max-width: 480px) {
  .trips-card {
    padding: 16px 20px;
  }
  
  .card-number {
    font-size: 18px;
  }
  
  .card-state,
  .card-location {
    padding: 4px 12px;
    font-size: 12px;
  }
  
  .info-item {
    padding: 8px 12px;
  }
  
  .info-label,
  .info-value {
    font-size: 13px;
  }
}
</style>