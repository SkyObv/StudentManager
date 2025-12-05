<script>
// 老师账号管理组件
export default {
  name: 'TeacherManage',
  data() {
    return {
      // 老师数据（静态数据）
      teachers: [
        {
          "id": 2,
          "username": "000000",
          "name": "大大怪",
          "gender": "male",
          "is_active": true,
          "counts": 1
        },
        {
          "id": 5,
          "username": "432234",
          "name": "迷糊老师",
          "gender": "male",
          "is_active": true,
          "counts": 1
        },
        {
          "id": 6,
          "username": "543345",
          "name": "李老师",
          "gender": "female",
          "is_active": true,
          "counts": 3
        },
        {
          "id": 7,
          "username": "654456",
          "name": "王老师",
          "gender": "male",
          "is_active": false,
          "counts": 2
        }
      ],

      // 筛选数据
      genderFilter: '',
      searchQuery: '',
      isActiveFilter: 'active', // 默认只显示活跃账号
      // 表单状态
      showAddTeacherForm: false,
      showDeleteTeacherForm: false,
      // 删除老师对话框
      teacherToDelete: null,
      // 新增老师表单数据
      newTeacher: {
        username: '',
        name: '',
        gender: 'male'
      },
      // 加载状态
      loading: false
    }
  },
  computed: {
    /**
     * 计算过滤后的老师数据
     * @returns {Array} 过滤后的老师数据
     */
    filteredTeachers() {
      let filtered = this.teachers;
      
      // 按账号状态过滤
      if (this.isActiveFilter === 'active') {
        filtered = filtered.filter(teacher => teacher.is_active === true);
      } else if (this.isActiveFilter === 'inactive') {
        filtered = filtered.filter(teacher => teacher.is_active === false);
      }
      
      // 按性别过滤
      if (this.genderFilter) {
        filtered = filtered.filter(teacher => teacher.gender === this.genderFilter);
      }
      
      // 按姓名搜索
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(teacher => 
          teacher.name.toLowerCase().includes(query) || 
          teacher.username.includes(query)
        );
      }
      
      return filtered;
    },

    /**
     * 获取性别显示文本映射
     * @returns {Object} 性别文本映射对象
     */
    genderText() {
      return {
        'male': '男',
        'female': '女'
      };
    },

    /**
     * 获取性别图标映射
     * @returns {Object} 性别图标映射对象
     */
    genderIcon() {
      return {
        'male': '♂',
        'female': '♀'
      };
    },

    /**
     * 获取账号状态映射
     * @returns {Object} 账号状态映射对象
     */
    accountStatus() {
      return {
        'true': { text: '启用', class: 'status-active' },
        'false': { text: '禁用', class: 'status-inactive' }
      };
    }
  },
  methods: {
    /**
     * 处理搜索和筛选
     */
    searchTeachers() {
      // 搜索时不需要分页
    },

    /**
     * 重置所有筛选条件
     */
    resetFilters() {
      this.genderFilter = '';
      this.searchQuery = '';
      this.isActiveFilter = 'active'; // 重置为默认显示活跃账号
    },

    /**
     * 打开添加老师表单
     */
    openAddTeacherForm() {
      this.showAddTeacherForm = true;
      // 重置表单数据
      this.newTeacher = {
        username: '',
        name: '',
        gender: 'male'
      };
    },

    /**
     * 关闭添加老师表单
     */
    closeAddTeacherForm() {
      this.showAddTeacherForm = false;
    },

    /**
     * 提交添加老师表单
     */
    submitAddTeacher() {
      // 验证表单数据
      if (!this.newTeacher.username || !this.newTeacher.name) {
        this.$message.warning('请填写完整的老师信息');
        return;
      }

      // 模拟添加老师（静态数据）
      const newTeacher = {
        id: Date.now(), // 使用时间戳作为临时ID
        ...this.newTeacher,
        is_active: true,
        counts: 0
      };

      // 添加到老师列表
      this.teachers.push(newTeacher);

      // 关闭表单
      this.closeAddTeacherForm();

      // 显示成功提示
      this.$message.success('老师账号创建成功');
    },

    /**
     * 打开删除老师表单
     * @param {Object} teacher - 要删除的老师对象
     */
    openDeleteTeacherForm(teacher) {
      this.teacherToDelete = teacher;
      this.showDeleteTeacherForm = true;
    },

    /**
     * 关闭删除老师表单
     */
    closeDeleteTeacherForm() {
      this.showDeleteTeacherForm = false;
      this.teacherToDelete = null;
    },

    /**
     * 提交删除老师操作
     */
    submitDeleteTeacher() {
      if (!this.teacherToDelete) return;

      // 模拟删除老师（静态数据）
      this.teachers = this.teachers.filter(teacher => teacher.id !== this.teacherToDelete.id);

      // 关闭表单
      this.closeDeleteTeacherForm();

      // 显示成功提示
      this.$message.success('老师账号删除成功');
    }
  }
}
</script>

<template>
  <div class="teacher-manage">
    <div class="content-container">
      <!-- 页面头部 -->
      <div class="page-header">
        <!-- 页面标题 -->
        <h1 class="page-title">老师账号管理</h1>
      </div>

    <!-- 筛选和搜索区域 -->
    <div class="filter-section">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索老师名字或账号..." 
          class="search-input"
        >
        <button class="search-button" @click="searchTeachers">
          <span class="search-icon">🔍</span>
          <span class="search-text">搜索</span>
        </button>
      </div>

      <div class="filter-controls">
        <select v-model="isActiveFilter" class="filter-select" @change="searchTeachers">
          <option value="">全部账号</option>
          <option value="active">活跃账号</option>
          <option value="inactive">禁用账号</option>
        </select>
        
        <select v-model="genderFilter" class="filter-select" @change="searchTeachers">
          <option value="">全部性别</option>
          <option value="male">男老师</option>
          <option value="female">女老师</option>
        </select>

        <button class="reset-button" @click="resetFilters">重置筛选</button>
      </div>

      <!-- 老师管理按钮 -->
      <div class="teacher-management">
        <button class="add-teacher-button" @click="openAddTeacherForm">
          <span class="button-icon">➕</span>
          <span class="button-text">创建老师账号</span>
        </button>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="stats-section">
      <div class="stat-item">
        <span class="stat-label">总老师数：</span>
        <span class="stat-value">{{ filteredTeachers.length }}</span>
      </div>
    </div>

    <!-- 老师列表 -->
    <div class="teachers-grid">
      <div class="teacher-card" v-for="teacher in filteredTeachers" :key="teacher.id">
        <!-- 删除老师按钮 -->
        <button class="delete-teacher-button" @click="openDeleteTeacherForm(teacher)" title="删除老师">
          🗑️
        </button>
        <!-- 卡片头部 -->
        <div class="card-header">
          <h3 class="teacher-name">{{ teacher.name }}</h3>
          <div :class="['account-status', accountStatus[teacher.is_active.toString()].class]">
            {{ accountStatus[teacher.is_active.toString()].text }}
          </div>
        </div>

        <!-- 老师信息 -->
        <div class="teacher-info">
          <div class="info-row">
            <span class="info-label">账号：</span>
            <span class="info-value">{{ teacher.username }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">性别：</span>
            <span class="info-value gender-badge" :class="teacher.gender">
              {{ genderIcon[teacher.gender] }} {{ genderText[teacher.gender] }}
            </span>
          </div>
          <div class="info-row">
            <span class="info-label">学生数：</span>
            <span class="info-value">{{ teacher.counts }}人</span>
          </div>
        </div>
      </div>

      <!-- 无老师数据时显示 -->
      <div class="no-teachers" v-if="filteredTeachers.length === 0">
        <p>暂无老师数据</p>
      </div>
    </div>
    </div>

    <!-- 添加老师对话框 -->
    <div class="modal" v-if="showAddTeacherForm">
      <div class="modal-content">
        <div class="modal-header">
          <h3>创建老师账号</h3>
          <button class="close-button" @click="closeAddTeacherForm">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitAddTeacher">
            <div class="form-group">
              <label for="teacher_username">账号：</label>
              <input type="text" id="teacher_username" v-model="newTeacher.username" required>
            </div>
            <div class="form-group">
              <label for="teacher_name">姓名：</label>
              <input type="text" id="teacher_name" v-model="newTeacher.name" required>
            </div>
            <div class="form-group">
              <label for="teacher_gender">性别：</label>
              <select id="teacher_gender" v-model="newTeacher.gender" required>
                <option value="male">男</option>
                <option value="female">女</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="cancel-button" @click="closeAddTeacherForm">取消</button>
              <button type="submit" class="submit-button">创建</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 删除老师对话框 -->
    <div class="modal" v-if="showDeleteTeacherForm">
      <div class="modal-content">
        <div class="modal-header">
          <h3>删除老师</h3>
          <button class="close-button" @click="closeDeleteTeacherForm">×</button>
        </div>
        <div class="modal-body">
          <div class="delete-confirm">
            <p>确定要删除老师 <strong>{{ teacherToDelete?.name }}</strong> 吗？</p>
            <p class="delete-warning">此操作不可恢复，请谨慎操作。</p>
          </div>
          <div class="form-actions">
            <button type="button" class="cancel-button" @click="closeDeleteTeacherForm">取消</button>
            <button type="button" class="delete-confirm-button" @click="submitDeleteTeacher">确认删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面容器 */
.teacher-manage {
  padding: 2rem;
  font-family: Arial, sans-serif;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
  animation: pageFadeIn 0.6s ease-out;
}

/* 内容容器 */
.content-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 3rem;
  color: #1e293b;
}

.page-title {
  font-size: 2.5rem;
  margin: 0;
  color: #333;
  font-weight: 800;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  animation: fadeInUp 0.8s ease-out;
}

/* 筛选和搜索区域 */
.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
  flex-wrap: wrap;
  gap: 10px;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.search-box {
  display: flex;
  align-items: center;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 14px;
}

.search-button {
  padding: 8px 16px;
  background-color: #409EFF;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.search-button:hover {
  background-color: #66B1FF;
}

.filter-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.reset-button {
  padding: 8px 16px;
  background-color: #909399;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.reset-button:hover {
  background-color: #A6A9AD;
}

.teacher-management {
  display: flex;
  gap: 10px;
}

.add-teacher-button {
  padding: 8px 16px;
  background-color: #67C23A;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.add-teacher-button:hover {
  background-color: #85CE61;
}

/* 统计信息 */
.stats-section {
  display: flex;
  gap: 30px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
  animation: fadeInUp 0.8s ease-out 0.3s both;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.stat-value {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

/* 老师列表 */
.teachers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
  animation: fadeInUp 0.8s ease-out 0.4s both;
}

/* 老师卡片 */
.teacher-card {
  position: relative;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: box-shadow 0.3s ease;
  animation: fadeInUp 0.8s ease-out 0.5s both;
}

.teacher-card:hover {
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
}

.delete-teacher-button {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: transparent;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: #909399;
  padding: 5px;
  border-radius: 4px;
  z-index: 10;
}

.delete-teacher-button:hover {
  background-color: #f56c6c;
  color: white;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding: 0 0 10px 30px; /* 增加左侧内边距，避免与删除按钮重叠 */
  border-bottom: 1px solid #eee;
}

.teacher-name {
  font-size: 18px;
  margin: 0;
  color: #333;
}

.account-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
}

.status-active {
  background-color: #f0f9eb;
  color: #67C23A;
}

.status-inactive {
  background-color: #fef0f0;
  color: #f56c6c;
}

/* 老师信息 */
.teacher-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-size: 14px;
  color: #606266;
}

.info-value {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.gender-badge {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}

.gender-badge.male {
  background-color: #e6f7ff;
  color: #1890ff;
}

.gender-badge.female {
  background-color: #fff0f6;
  color: #f5222d;
}

/* 无老师数据 */
.no-teachers {
  grid-column: 1 / -1;
  text-align: center;
  padding: 50px;
  color: #909399;
}



/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  animation: modalSlideIn 0.3s ease;
}

/* 页面加载动画 */
@keyframes pageFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 渐入动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 模态框动画 */
@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
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
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #909399;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.close-button:hover {
  background-color: #f5f5f5;
  color: #606266;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.cancel-button {
  padding: 8px 16px;
  background-color: #909399;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.cancel-button:hover {
  background-color: #A6A9AD;
}

.submit-button {
  padding: 8px 16px;
  background-color: #409EFF;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.submit-button:hover {
  background-color: #66B1FF;
}

.delete-confirm-button {
  padding: 8px 16px;
  background-color: #f56c6c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.delete-confirm-button:hover {
  background-color: #f78989;
}

.delete-confirm {
  margin-bottom: 20px;
}

.delete-warning {
  color: #f56c6c;
  margin-top: 10px;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .filter-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box,
  .filter-controls,
  .teacher-management {
    width: 100%;
    justify-content: center;
  }
  
  .teachers-grid {
    grid-template-columns: 1fr;
  }
}
</style>