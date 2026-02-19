<script>
export default {
  name: 'HostelInfoCard',
  props: {
    // [
    //   {
    //     "id": 1,
    //     "floor": "1",
    //     "hostel_number": "101",
    //     "gender": "male",
    //     "students": [
    //         {
    //             "id": 3,
    //             "name": "奥特曼银河",
    //             "gender": "male"
    //             "userneam": "123456"
    //         }
    //     ]
    //   }
    // ]
    hostel: {
        type: Object,
        required: true
    },
    isSelected: {                                                    // 是否被选中
        type: Boolean,
        default: false
    }
  },
  computed: {
    // 性别显示文本映射
    genderText() {
      return {
        'male': '男生宿舍',
        'female': '女生宿舍'
      };
    },
    // 性别图标映射
    genderIcon() {
      return {
        'male': '♂',
        'female': '♀'
      };
    },
    // 房间状态映射
    roomStatus() {
      return {
        'true': { text: '已满', class: 'status-full' },
        'false': { text: '有空位', class: 'status-available' }
      };
    }
  },
  methods: {
    // 发送添加学生事件
    addStudent() {
      this.$emit('addStudent',);
    },
    // 发送删除学生事件
    deleteStudent(student) {
      this.$emit('deleteStudent',student);
    },
    myClick() {                                                      // 我被点击了
      this.$emit('myClick', this.hostel);
    }
  }
};
</script>

<template>
  <div class="hostel-card" :class="{ 'hostel-card-selected': isSelected }" @click="myClick">
    <!-- 卡片头部 -->
    <div class="card-header">
      <h3 class="hostel-number">{{ hostel.hostel_number }}</h3>
      <div :class="['room-status', roomStatus[(hostel.is_full ? hostel.is_full.toString() : 'false')].class]">
        {{ roomStatus[(hostel.is_full ? hostel.is_full.toString() : 'false')].text }}
      </div>
    </div>
    
    <!-- 宿舍信息 -->
    <div class="hostel-info">
      <div class="info-row">
        <span class="info-label">楼层：</span>
        <span class="info-value">{{ hostel.floor }}楼</span>
      </div>
      <div class="info-row">
        <span class="info-label">性别：</span>
        <span class="info-value gender-badge" :class="hostel.gender">
          {{ genderIcon[hostel.gender] }} {{ genderText[hostel.gender] }}
        </span>
      </div>
      <div class="info-row">
        <span class="info-label">学生人数：</span>
        <span class="info-value">{{ hostel.students && hostel.students.length ? hostel.students.length : 0 }}人</span>
      </div>
      <div class="info-row">
        <span class="info-label">宿舍管理员：</span>
        <span class="info-value">
          <span v-if="hostel.manager">{{ hostel.manager }}</span>
          <span v-else class="no-manager">无</span>
        </span>
      </div>
    </div>
    
    <!-- 学生列表 -->
    <div class="students-section">
      <h4 class="section-title">入住学生</h4>
      <div class="students-list" v-if="hostel.students && hostel.students.length > 0">
        <div class="student-item" v-for="student in hostel.students" :key="student.id">
          <span class="student-name">{{ student.name }}</span>
          <span class="student-gender" :class="student.gender">
            {{ genderIcon[student.gender] }}
          </span>
          <!-- 删除学生按钮 -->
          <button class="delete-student-button" @click="deleteStudent(student)" title="删除学生">
            🗑️
          </button>
        </div>
      </div>
      <div class="no-students" v-else>
        <p>暂无学生入住</p>
      </div>
    </div>
    
    <!-- 操作按钮 -->
    <div class="card-actions">
      <button class="add-student-button" @click="addStudent">
        <span class="button-icon">➕</span>
        添加学生
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

/* 选中状态的卡片 */
.hostel-card-selected {
  border: 4px solid #3b82f6;
  box-shadow: 0 0 25px rgba(59, 130, 246, 0.4);
  transform: translateY(-3px);
  animation: pulse-border 2s infinite;
}

.hostel-card-selected::before {
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  height: 6px;
}

/* 边框脉冲动画 */
@keyframes pulse-border {
  0% {
    box-shadow: 0 0 25px rgba(59, 130, 246, 0.4);
  }
  50% {
    box-shadow: 0 0 35px rgba(59, 130, 246, 0.6);
  }
  100% {
    box-shadow: 0 0 25px rgba(59, 130, 246, 0.4);
  }
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

.room-status {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.status-full {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2);
}

.status-available {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
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

/* 学生列表 */
.students-section {
  margin-bottom: 25px;
  flex: 1;
  min-height: 120px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #374151;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title::before {
  content: "👥";
  font-size: 16px;
}

.students-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.student-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #ffffff, #f8fafc);
  border-radius: 20px;
  font-size: 14px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.student-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
  border-color: #3b82f6;
}

.student-name {
  color: #1e293b;
  font-weight: 600;
}

.student-gender {
  font-size: 16px;
  font-weight: bold;
}

.student-gender.male {
  color: #3b82f6;
}

.student-gender.female {
  color: #db2777;
}

/* 删除学生按钮 */
.delete-student-button {
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-left: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-student-button:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.no-students {
  color: #94a3b8;
  font-style: italic;
  text-align: center;
  padding: 15px;
  background: linear-gradient(135deg, #f8fafc, #ffffff);
  border-radius: 8px;
  border: 1px dashed #cbd5e1;
  font-size: 14px;
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

.add-student-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 24px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  min-width: 120px;
  justify-content: center;
  line-height: 20px;
  min-height: 40px;
}

.add-student-button:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.button-icon {
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 767px) {
  .hostel-card {
    padding: 20px;
    padding-top: 40px;
  }
  
  .hostel-number {
    font-size: 20px;
  }
}
</style>