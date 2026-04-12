<script>
export default {
  name: 'StudentsTable',
  props: {
    students: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      editingId: null,
      editForm: {
        key_number: '',
        key_state: false
      }
    }
  },
  computed: {
    hasStudents() {
      return this.students && this.students.length > 0;
    }
  },
  methods: {
    getKeyStateText(state) {                                       // 获取门禁卡状态文本
      return state ? '正常' : '禁用';
    },
    getKeyStateClass(state) {                                      // 获取门禁卡状态样式类
      return state ? 'state-normal' : 'state-disabled';
    },
    startEdit(student) {                                            // 开始编辑
      this.editingId = student.id;
      this.editForm = {
        key_number: student.key_number || '',
        key_state: student.key_state || false
      };
    },
    cancelEdit() {                                                  // 取消编辑
      this.editingId = null;
      this.editForm = {
        key_number: '',
        key_state: false
      };
    },
    saveEdit(student) {                                            // 保存编辑
      this.$emit('update-key', {
        id: student.id,
        key_number: this.editForm.key_number,
        key_state: this.editForm.key_state
      });
      this.cancelEdit();
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
          <th>门禁id</th>
          <th>门禁卡状态</th>
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
          <td>{{ student.key_number }}</td>
          <td>
            <span :class="getKeyStateClass(student.key_state)">
              {{ getKeyStateText(student.key_state) }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
    
    <!-- 无数据提示 -->
    <div class="empty-data" v-else>
      <div class="empty-icon">📚</div>
      <p>暂无学生数据</p>
    </div>

    <!-- 编辑弹窗 -->
    <div class="edit-modal-overlay" v-if="editingId" @click.self="cancelEdit">
      <div class="edit-modal">
        <div class="modal-header">
          <h3>编辑门禁信息</h3>
          <button class="btn-close" @click="cancelEdit">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>门禁ID</label>
            <input type="text" v-model="editForm.key_number" placeholder="请输入门禁ID" />
          </div>
          <div class="form-group">
            <label>门禁卡状态</label>
            <div class="switch-container">
              <span :class="{ active: !editForm.key_state }">禁用</span>
              <label class="switch">
                <input type="checkbox" v-model="editForm.key_state" />
                <span class="slider"></span>
              </label>
              <span :class="{ active: editForm.key_state }">正常</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="cancelEdit">取消</button>
          <button class="btn-save" @click="saveEdit(students.find(s => s.id === editingId))">保存</button>
        </div>
      </div>
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

.state-normal {
  color: #67c23a;
  font-weight: 500;
}

.state-disabled {
  color: #f56c6c;
  font-weight: 500;
}

.action-btns {
  display: flex;
  gap: 8px;
}

.btn-edit {
  padding: 6px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s ease;
}

.btn-edit:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.edit-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.edit-modal {
  background: white;
  border-radius: 16px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #ebeef5;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #909399;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: color 0.3s;
}

.btn-close:hover {
  color: #303133;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.form-group input[type="text"] {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.form-group input[type="text"]:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.switch-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.switch-container span {
  font-size: 14px;
  color: #909399;
  transition: color 0.3s;
}

.switch-container span.active {
  color: #667eea;
  font-weight: 500;
}

.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 26px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #dcdfe6;
  transition: 0.3s;
  border-radius: 26px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input:checked + .slider {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

input:checked + .slider:before {
  transform: translateX(24px);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #ebeef5;
}

.btn-cancel,
.btn-save {
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel {
  background: #f5f7fa;
  border: 1px solid #dcdfe6;
  color: #606266;
}

.btn-cancel:hover {
  background: #e9ecf0;
}

.btn-save {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

.btn-save:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
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