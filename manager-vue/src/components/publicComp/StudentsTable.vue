<script>
// 我的学生表格
export default {
  name: 'StudentsTable',
  props: {
    students: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    // 检查是否有学生数据
    hasStudents() {
      return this.students && this.students.length > 0;
    }
  }
}
</script>

<template>
  <div class="students-table-container">
    <!-- 学生列表表格 -->
    <table class="students-table" v-if="hasStudents">
      <thead>
        <tr>
          <th>学号</th>
          <th>姓名</th>
          <th>性别</th>
          <th>宿舍</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.id">
          <td>{{ student.username }}</td>
          <td>{{ student.name }}</td>
          <td :class="{'gender-male': student.gender === 'male', 'gender-female': student.gender === 'female'}">
            {{ student.gender === 'male' ? '男' : '女' }}
          </td>
          <td>{{ student.house_number || '无' }}</td>
        </tr>
      </tbody>
    </table>
    
    <!-- 无数据提示 -->
    <div class="empty-data" v-else>
      <div class="empty-icon">📚</div>
      <p>暂无学生数据</p>
    </div>
  </div>
</template>

<style scoped>
/* 表格容器 */
.students-table-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
  overflow: hidden;
  animation: fadeIn 0.6s ease-out;
}

/* 表格样式 */
.students-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
}

.students-table th, .students-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
  font-size: 14px;
}

.students-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #606266;
  white-space: nowrap;
}

.students-table td {
  color: #303133;
}

.students-table tr {
  transition: all 0.3s ease;
}

.students-table tr:hover {
  background-color: rgba(102, 126, 234, 0.05);
}

.students-table tr:last-child td {
  border-bottom: none;
}

/* 性别显示样式 */
.gender-male {
  color: #409eff;
  font-weight: 500;
}

.gender-female {
  color: #f77295;
  font-weight: 500;
}

/* 无数据状态 */
.empty-data {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
  color: #909399;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-data p {
  margin: 0;
  font-size: 16px;
}

/* 动画关键帧 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .students-table-container {
    overflow-x: auto;
  }
  
  .students-table {
    min-width: 600px;
  }
  
  .students-table th, .students-table td {
    padding: 12px 16px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .students-table th, .students-table td {
    padding: 10px 12px;
  }
  
  .empty-data {
    padding: 40px 20px;
  }
}
</style>