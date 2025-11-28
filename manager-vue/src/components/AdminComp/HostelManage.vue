<script>
export default {
  name: 'HostelManage',
  data() {
    return {
      // 静态宿舍数据
      hostels_data: [
        {
          "hostel_number": "101",
          "floor": 1,
          "student_count": 1,
          "is_full": false,
          "gender": "male",
          "students": [
            {
              "id": 3,
              "name": "小小怪",
              "gender": "male"
            }
          ]
        },
        {
          "hostel_number": "102",
          "floor": 1,
          "student_count": 1,
          "is_full": false,
          "gender": "male",
          "students": [
            {
              "id": 4,
              "name": "小猪猪",
              "gender": "male"
            }
          ]
        },
        {
          "hostel_number": "103",
          "floor": 1,
          "student_count": 0,
          "is_full": false,
          "gender": "male",
          "students": []
        }
      ],
      // 分页数据
      currentPage: 1,
      pageSize: 20,
      // 筛选数据
      genderFilter: '',
      searchQuery: '',
      // 表单状态
      showAddHostelForm: false,
      showAddStudentForm: false,
      showDeleteStudentForm: false,
      // 新增宿舍表单数据
      newHostel: {
        hostel_number: '',
        floor: 1,
        gender: 'male'
      },
      selectedHostel: null,
      selectedStudent: null,
      // 新增学生表单数据
      newStudent: {
        name: '',
        gender: 'male'
      }
    }
  },
  computed: {
    /**
     * 计算总页数
     * @returns {number} 总页数
     */
    totalPages() {
      return Math.ceil(this.totalCount / this.pageSize);
    },
    
    /**
     * 根据搜索条件和性别过滤的宿舍列表
     * @returns {Array} 过滤后的宿舍列表
     */
    filteredHostels() {
      let result = this.hostels_data;
      
      // 根据宿舍号进行搜索筛选
      if (this.searchQuery) {
        result = result.filter(hostel => 
          hostel.hostel_number.includes(this.searchQuery)
        );
      }
      
      // 根据性别进行筛选
      if (this.genderFilter) {
        result = result.filter(hostel => hostel.gender === this.genderFilter);
      }
      
      return result;
    },
    
    /**
     * 获取过滤后的宿舍总记录数
     * @returns {number} 总记录数
     */
    totalCount() {
      return this.filteredHostels.length;
    },
    
    /**
     * 获取当前页显示的宿舍数据
     * @returns {Array} 当前页的宿舍列表
     */
    currentHostels() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredHostels.slice(start, end);
    },
    
    /**
     * 获取性别显示文本映射
     * @returns {Object} 性别文本映射对象
     */
    genderText() {
      return {
        'male': '男生宿舍',
        'female': '女生宿舍'
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
     * 获取房间状态映射
     * @returns {Object} 房间状态映射对象
     */
    roomStatus() {
      return {
        'true': { text: '已满', class: 'status-full' },
        'false': { text: '有空位', class: 'status-available' }
      };
    }
  },
  methods: {
    /**
     * 返回楼层管理页面
     * 触发父组件的goBack事件
     */
    goBack() {
      this.$emit('goBack');
    },
    
    /**
     * 处理分页页码变化
     * @param {number} page - 新的页码
     */
    handlePageChange(page) {
      this.currentPage = page;
    },
    
    /**
     * 跳转到上一页
     * 如果当前不是第一页，则页码减1
     */
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    
    /**
     * 跳转到下一页
     * 如果当前不是最后一页，则页码加1
     */
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    
    /**
     * 跳转到指定页码
     * @param {number} page - 要跳转到的页码
     */
    goToPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    
    /**
     * 重置所有筛选条件
     * 清空搜索框、性别筛选，并回到第一页
     */
    resetFilters() {
      this.genderFilter = '';
      this.searchQuery = '';
      this.currentPage = 1;
    },
    
    /**
     * 执行搜索操作
     * 重置页码到第一页，搜索逻辑通过computed属性自动处理
     */
    searchHostels() {
      // 搜索逻辑已通过computed属性filteredHostels自动实现
      this.currentPage = 1; // 搜索时重置到第一页
    },
    
    /**
     * 打开新建宿舍表单
     * 重置表单数据并显示模态框
     */
    openAddHostelForm() {
      // 重置新建宿舍表单数据
      this.newHostel = {
        hostel_number: '',
        floor: 1,
        gender: 'male'
      };
      // 显示新建宿舍表单
      this.showAddHostelForm = true;
    },
    
    /**
     * 关闭新建宿舍表单
     * 隐藏模态框
     */
    closeAddHostelForm() {
      this.showAddHostelForm = false;
    },
    
    /**
     * 提交新建宿舍表单
     * 验证数据，检查宿舍号是否已存在，添加新宿舍到数据列表
     */
    submitAddHostel() {
      // 验证宿舍号是否为空
      if (!this.newHostel.hostel_number) {
        alert('请输入宿舍号');
        return;
      }
      
      // 检查宿舍号是否已存在
      if (this.hostels_data.some(h => h.hostel_number === this.newHostel.hostel_number)) {
        alert('宿舍号已存在');
        return;
      }
      
      // 构建新宿舍完整数据
      const newHostelData = {
        ...this.newHostel,
        student_count: 0, // 初始学生数为0
        is_full: false,   // 初始状态为未满
        students: []      // 初始没有学生
      };
      
      // 添加新宿舍到数据列表
      this.hostels_data.push(newHostelData);
      // 关闭表单
      this.showAddHostelForm = false;
      // 显示成功提示
      alert('宿舍添加成功');
    },
    
    /**
     * 删除指定宿舍
     * @param {string} hostelNumber - 要删除的宿舍号
     */
    deleteHostel(hostelNumber) {
      // 确认删除操作
      if (confirm('确定要删除这个宿舍吗？')) {
        // 查找宿舍索引
        const index = this.hostels_data.findIndex(h => h.hostel_number === hostelNumber);
        // 如果找到宿舍，则删除
        if (index !== -1) {
          this.hostels_data.splice(index, 1);
          // 显示成功提示
          alert('宿舍删除成功');
        }
      }
    },
    
    /**
     * 打开添加学生表单
     * @param {Object} hostel - 目标宿舍对象
     */
    openAddStudentForm(hostel) {
      // 设置当前选中的宿舍
      this.selectedHostel = hostel;
      // 重置添加学生表单数据，默认性别与宿舍一致
      this.newStudent = {
        name: '',
        gender: hostel.gender
      };
      // 显示添加学生表单
      this.showAddStudentForm = true;
    },
    
    /**
     * 关闭添加学生表单
     * 隐藏模态框并清空选中的宿舍
     */
    closeAddStudentForm() {
      this.showAddStudentForm = false;
      this.selectedHostel = null;
    },
    
    /**
     * 提交添加学生表单
     * 验证数据，检查宿舍是否已满，添加学生到宿舍
     */
    submitAddStudent() {
      // 验证学生姓名是否为空
      if (!this.newStudent.name) {
        alert('请输入学生姓名');
        return;
      }
      
      // 检查宿舍是否已满
      if (this.selectedHostel.is_full) {
        alert('宿舍已满，无法添加学生');
        return;
      }
      
      // 生成新学生ID（当前最大ID+1）
      const maxId = Math.max(...this.hostels_data.flatMap(h => h.students.map(s => s.id)), 0);
      const newStudentData = {
        ...this.newStudent,
        id: maxId + 1
      };
      
      // 查找当前选中宿舍的索引
      const hostelIndex = this.hostels_data.findIndex(h => h.hostel_number === this.selectedHostel.hostel_number);
      if (hostelIndex !== -1) {
        // 添加学生到宿舍
        this.hostels_data[hostelIndex].students.push(newStudentData);
        // 更新学生人数
        this.hostels_data[hostelIndex].student_count += 1;
        // 检查是否已满（假设每个宿舍最多4人）
        if (this.hostels_data[hostelIndex].student_count >= 4) {
          this.hostels_data[hostelIndex].is_full = true;
        }
        // 关闭表单
        this.showAddStudentForm = false;
        // 显示成功提示
        alert('学生添加成功');
      }
    },
    
    /**
     * 打开删除学生表单
     * @param {Object} hostel - 学生所在宿舍对象
     * @param {Object} student - 要删除的学生对象
     */
    openDeleteStudentForm(hostel, student) {
      // 设置当前选中的宿舍和学生
      this.selectedHostel = hostel;
      this.selectedStudent = student;
      // 显示删除学生确认表单
      this.showDeleteStudentForm = true;
    },
    
    /**
     * 关闭删除学生表单
     * 隐藏模态框并清空选中的宿舍和学生
     */
    closeDeleteStudentForm() {
      this.showDeleteStudentForm = false;
      this.selectedHostel = null;
      this.selectedStudent = null;
    },
    
    /**
     * 提交删除学生操作
     * 确认删除后从宿舍中移除学生
     */
    submitDeleteStudent() {
      // 确认删除操作
      if (confirm(`确定要删除学生 ${this.selectedStudent.name} 吗？`)) {
        // 查找当前选中宿舍的索引
        const hostelIndex = this.hostels_data.findIndex(h => h.hostel_number === this.selectedHostel.hostel_number);
        if (hostelIndex !== -1) {
          // 查找要删除的学生索引
          const studentIndex = this.hostels_data[hostelIndex].students.findIndex(s => s.id === this.selectedStudent.id);
          if (studentIndex !== -1) {
            // 从宿舍中删除学生
            this.hostels_data[hostelIndex].students.splice(studentIndex, 1);
            // 更新学生人数
            this.hostels_data[hostelIndex].student_count -= 1;
            // 重置满员状态（如果之前是满员的）
            if (this.hostels_data[hostelIndex].is_full) {
              this.hostels_data[hostelIndex].is_full = false;
            }
            // 关闭表单
            this.showDeleteStudentForm = false;
            // 显示成功提示
            alert('学生删除成功');
          }
        }
      }
    }
  },

}
</script>

<template>
  <div class="hostel-manage">
    <!-- 页面头部 -->
    <div class="page-header">
      <!-- 返回按钮 -->
      <button class="back-button" @click="goBack">
        <span class="back-icon">←</span> 
        <span class="back-text">返回楼层管理</span>
      </button>
      
      <!-- 页面标题 -->
      <h1 class="page-title">宿舍详情页</h1>
    </div>
    
    <!-- 筛选和搜索区域 -->
    <div class="filter-section">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索宿舍号..." 
          class="search-input"
        >
        <button class="search-button" @click="searchHostels">
          <span class="search-icon">🔍</span>
          <span class="search-text">搜索</span>
        </button>
      </div>
      
      <div class="filter-controls">
        <select v-model="genderFilter" class="filter-select">
          <option value="">全部性别</option>
          <option value="male">男生宿舍</option>
          <option value="female">女生宿舍</option>
        </select>
        
        <button class="reset-button" @click="resetFilters">重置筛选</button>
      </div>
      
      <!-- 宿舍管理按钮 -->
      <div class="hostel-management">
        <button class="add-hostel-button" @click="openAddHostelForm">
          <span class="button-icon">➕</span>
          <span class="button-text">新建宿舍</span>
        </button>
      </div>
    </div>
    
    <!-- 统计信息 -->
    <div class="stats-section">
      <div class="stat-item">
        <span class="stat-label">总宿舍数：</span>
        <span class="stat-value">{{ totalCount }}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">当前页：</span>
        <span class="stat-value">{{ currentPage }} / {{ totalPages || 1 }}</span>
      </div>
    </div>
    
    <!-- 宿舍列表 -->
    <div class="hostels-grid">
      <div class="hostel-card" v-for="hostel in currentHostels" :key="hostel.hostel_number">
        <!-- 删除宿舍按钮 -->
        <button class="delete-hostel-button" @click="deleteHostel(hostel.hostel_number)" title="删除宿舍">
          🗑️
        </button>
        <!-- 卡片头部 -->
        <div class="card-header">
          <h3 class="hostel-number">{{ hostel.hostel_number }}</h3>
          <div :class="['room-status', roomStatus[hostel.is_full.toString()].class]">
            {{ roomStatus[hostel.is_full.toString()].text }}
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
            <span class="info-value">{{ hostel.student_count }}人</span>
          </div>
        </div>
        
        <!-- 学生列表 -->
        <div class="students-section">
          <h4 class="section-title">入住学生</h4>
          <div class="students-list" v-if="hostel.students.length > 0">
            <div class="student-item" v-for="student in hostel.students" :key="student.id">
              <span class="student-name">{{ student.name }}</span>
              <span class="student-gender" :class="student.gender">
                {{ genderIcon[student.gender] }}
              </span>
              <!-- 删除学生按钮 -->
              <button class="delete-student-button" @click="openDeleteStudentForm(hostel, student)" title="删除学生">
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
          <button class="add-student-button" @click="openAddStudentForm(hostel)" :disabled="hostel.is_full">
            <span class="button-icon">➕</span>
            添加学生
          </button>
        </div>
      </div>
    </div>
    
    <!-- 无数据提示 -->
    <div class="no-data" v-if="currentHostels.length === 0">
      <p>暂无符合条件的宿舍数据</p>
    </div>
    
    <!-- 新建宿舍表单 -->
    <div class="modal" v-if="showAddHostelForm">
      <div class="modal-content">
        <div class="modal-header">
          <h3>新建宿舍</h3>
          <button class="close-button" @click="closeAddHostelForm">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitAddHostel">
            <div class="form-group">
              <label for="hostel_number">宿舍号：</label>
              <input type="text" id="hostel_number" v-model="newHostel.hostel_number" required>
            </div>
            <div class="form-group">
              <label for="floor">楼层：</label>
              <input type="number" id="floor" v-model.number="newHostel.floor" min="1" required>
            </div>
            <div class="form-group">
              <label for="gender">性别：</label>
              <select id="gender" v-model="newHostel.gender" required>
                <option value="male">男生宿舍</option>
                <option value="female">女生宿舍</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="cancel-button" @click="closeAddHostelForm">取消</button>
              <button type="submit" class="submit-button">提交</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- 添加学生表单 -->
    <div class="modal" v-if="showAddStudentForm">
      <div class="modal-content">
        <div class="modal-header">
          <h3>添加学生 - {{ selectedHostel?.hostel_number }}</h3>
          <button class="close-button" @click="closeAddStudentForm">×</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitAddStudent">
            <div class="form-group">
              <label for="student_name">学生姓名：</label>
              <input type="text" id="student_name" v-model="newStudent.name" required>
            </div>
            <div class="form-group">
              <label for="student_gender">性别：</label>
              <select id="student_gender" v-model="newStudent.gender" required>
                <option value="male" :disabled="selectedHostel?.gender !== 'male'">男生</option>
                <option value="female" :disabled="selectedHostel?.gender !== 'female'">女生</option>
              </select>
            </div>
            <div class="form-actions">
              <button type="button" class="cancel-button" @click="closeAddStudentForm">取消</button>
              <button type="submit" class="submit-button">提交</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- 删除学生表单 -->
    <div class="modal" v-if="showDeleteStudentForm">
      <div class="modal-content">
        <div class="modal-header">
          <h3>删除学生</h3>
          <button class="close-button" @click="closeDeleteStudentForm">×</button>
        </div>
        <div class="modal-body">
          <div class="delete-confirm">
            <p>确定要删除学生 <strong>{{ selectedStudent?.name }}</strong> 吗？</p>
            <p class="delete-warning">此操作不可恢复，请谨慎操作。</p>
          </div>
          <div class="form-actions">
            <button type="button" class="cancel-button" @click="closeDeleteStudentForm">取消</button>
            <button type="button" class="delete-confirm-button" @click="submitDeleteStudent">确认删除</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 分页控件 -->
    <div class="pagination" v-if="totalCount > 0">
      <button 
        class="page-button" 
        :disabled="currentPage === 1"
        @click="prevPage"
      >
        上一页
      </button>
      
      <div class="page-numbers">
        <!-- 第一页 -->
        <button 
          class="page-number" 
          :class="{ active: currentPage === 1 }"
          @click="goToPage(1)"
        >
          1
        </button>
        
        <!-- 省略号 -->
        <span v-if="currentPage > 3" class="page-ellipsis">...</span>
        
        <!-- 当前页附近的页码 -->
        <button 
          v-for="page in Math.min(Math.max(2, currentPage - 1), totalPages - 1)" 
          :key="page"
          class="page-number" 
          :class="{ active: currentPage === page }"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
        
        <!-- 省略号 -->
        <span v-if="currentPage < totalPages - 2" class="page-ellipsis">...</span>
        
        <!-- 最后一页 -->
        <button 
          v-if="totalPages > 1"
          class="page-number" 
          :class="{ active: currentPage === totalPages }"
          @click="goToPage(totalPages)"
        >
          {{ totalPages }}
        </button>
      </div>
      
      <button 
        class="page-button" 
        :disabled="currentPage === totalPages"
        @click="nextPage"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<style scoped>
.hostel-manage {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 页面头部 */
.page-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

/* 返回按钮 */
.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: 15px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.back-button:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.back-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.3);
}

.back-icon {
  font-size: 18px;
  font-weight: bold;
}

.back-text {
  font-size: 14px;
  font-weight: 500;
}

/* 页面标题 */
.page-title {
  color: #1e293b;
  font-size: 32px;
  font-weight: 800;
  margin: 0;
  text-align: center;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
}

/* 筛选区域 */
.filter-section {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  padding: 20px;
  background: linear-gradient(135deg, #f8fafc, #ffffff);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.search-box {
  flex: 1;
  max-width: 400px;
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.search-input::placeholder {
  color: #94a3b8;
  font-weight: 400;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  transform: translateY(-1px);
}

.search-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.search-button:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.search-button .search-icon {
  font-size: 16px;
}

.search-button .search-text {
  font-size: 14px;
  font-weight: 500;
}

.filter-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* 宿舍管理按钮 */
.hostel-management {
  display: flex;
  gap: 10px;
  align-items: center;
}

.add-hostel-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 20px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

.add-hostel-button:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.button-icon {
  font-size: 14px;
}

.button-text {
  font-size: 14px;
  font-weight: 500;
}

.filter-select {
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  background: white;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  min-width: 120px;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.reset-button {
  padding: 12px 20px;
  background: linear-gradient(135deg, #64748b, #475569);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(100, 116, 139, 0.3);
}

.reset-button:hover {
  background: linear-gradient(135deg, #475569, #334155);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(100, 116, 139, 0.4);
}

/* 统计信息 */
.stats-section {
  display: flex;
  gap: 30px;
  margin-bottom: 25px;
  padding: 15px 0;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  padding: 12px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border-left: 3px solid #3b82f6;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

/* 宿舍卡片网格 */
.hostels-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 25px;
  margin-bottom: 40px;
}

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
  padding-right: 40px; /* 为删除按钮留出空间 */
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

/* 学生列表 */
.students-section {
  margin-bottom: 25px;
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

.delete-hostel-button {
  position: absolute;
  top: 15px;
  right: 10px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
  z-index: 10;
}

.delete-hostel-button:hover {
  background: #dc2626;
  opacity: 1;
  transform: scale(1.1);
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
  padding-top: 20px;
  border-top: 1px solid #f1f5f9;
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
}

.add-student-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.add-student-button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* 无数据提示 */
.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
  background: linear-gradient(135deg, #f8fafc, #ffffff);
  border-radius: 16px;
  border: 2px dashed #cbd5e1;
  margin-bottom: 30px;
  transition: all 0.3s ease;
}

.no-data:hover {
  border-color: #94a3b8;
  background: #f1f5f9;
}

.no-data p {
  font-size: 16px;
  font-weight: 500;
  margin: 0;
}

/* 分页控件 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin-top: 40px;
  padding: 15px;
  background: linear-gradient(135deg, #f8fafc, #ffffff);
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.page-button {
  padding: 10px 18px;
  background: linear-gradient(135deg, #ffffff, #f1f5f9);
  color: #374151;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.page-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
}

.page-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.page-numbers {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-number {
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #ffffff, #f8fafc);
  color: #374151;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.page-number:hover {
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
}

.page-number.active {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border-color: #3b82f6;
  font-weight: 600;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.page-ellipsis {
  color: #94a3b8;
  font-size: 18px;
  padding: 0 8px;
  font-weight: 300;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border-bottom: 2px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.modal-body {
  padding: 20px;
}

/* 表单样式 */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 30px;
}

.cancel-button {
  padding: 10px 20px;
  background: #64748b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-button:hover {
  background: #475569;
}

.submit-button {
  padding: 10px 20px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background: linear-gradient(135deg, #059669, #047857);
}

.delete-confirm-button {
  padding: 10px 20px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-confirm-button:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
}

.delete-confirm {
  padding: 15px;
  background: #fef2f2;
  border: 1px solid #fee2e2;
  border-radius: 8px;
  margin-bottom: 20px;
}

.delete-confirm p {
  margin: 0 0 10px 0;
  color: #7f1d1d;
}

.delete-warning {
  font-weight: 600;
  color: #ef4444 !important;
}

/* 响应式设计 */
@media (min-width: 768px) {
  .hostels-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }
  
  .filter-section {
    flex-direction: row;
  }
  
  .stats-section {
    flex-direction: row;
  }
}

@media (max-width: 767px) {
  .hostel-manage {
    padding: 15px;
  }
  
  /* 页面头部 */
  .page-header {
    padding-bottom: 15px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  /* 返回按钮 */
  .back-button {
    padding: 8px 16px;
    border-radius: 40px;
  }
  
  /* 筛选区域 */
  .filter-section {
    flex-direction: column;
    gap: 12px;
    padding: 15px;
  }
  
  .search-box {
    max-width: 100%;
    flex-direction: column;
  }
  
  .search-button {
    width: 100%;
  }
  
  .filter-controls {
    flex-direction: column;
    width: 100%;
  }
  
  .filter-select,
  .reset-button {
    width: 100%;
  }
  
  .hostel-management {
    width: 100%;
  }
  
  .add-hostel-button {
    width: 100%;
  }
  
  /* 统计信息 */
  .stats-section {
    flex-direction: column;
    gap: 10px;
  }
  
  .stat-item {
    padding: 8px 12px;
  }
  
  /* 宿舍卡片 */
  .hostel-card {
    padding: 20px;
    padding-top: 40px;
  }
  
  .hostel-number {
    font-size: 20px;
  }
  
  /* 分页控件 */
  .pagination {
    gap: 8px;
    padding: 8px;
  }
  
  .page-button {
    padding: 8px 14px;
    font-size: 12px;
  }
  
  .page-number {
    width: 32px;
    height: 32px;
    font-size: 12px;
  }
  
  /* 模态框 */
  .modal {
    padding: 10px;
  }
  
  .modal-content {
    max-height: 90vh;
    overflow-y: auto;
  }
  
  .modal-body {
    padding: 15px;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .cancel-button,
  .submit-button,
  .delete-confirm-button {
    width: 100%;
  }
}
</style>