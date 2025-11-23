<script>
export default {
  name: 'StudentManagement',
  data() {
    return {
      request_url:`${this.$settings.Host}/admin_manager/getStuidents/`,
      page:1,                                                        // 当前页码
      page_count:null,                                               // 总页数
      students:[],                                                   // 学生列表
      count:null,                                                    // 学生总数
    }
  },
  created() {
    this.getStudents()
  },
  methods:{
    // 页码切换
    changePage(index){
      if(index === this.page){return "page-btn page-btn-active"}else {return "page-btn"}
    },
    // 获取学生列表
    getStudents(index){
      if (index){this.request_url = `${this.$settings.Host}/admin_manager/getStuidents/?page=${index}`;this.page =  index}
      this.$axios.get(this.request_url).then(res => {
        this.students = res.data.results
        this.count = res.data.count
        this.page_count = Math.ceil(res.data.count / 20)
        window.scrollTo({
        top: 0,
        behavior: 'smooth'
        });
      })
    }
  }
}
</script>

<template>
  <div class="student-management">
    <!-- 学生管理标题 -->
    <div class="management-header">
      <h2>学生管理</h2>
    </div>

    <!-- 筛选条件区域 -->
    <div class="filter-section">
      <div class="filter-controls">
        <!-- 年级筛选 -->
        <div class="filter-group">
          <label class="filter-label">年级：</label>
          <div class="grade-buttons">
            <button class="grade-btn">初一</button>
            <button class="grade-btn">初二</button>
            <button class="grade-btn">初三</button>
            <button class="grade-btn grade-btn-all">全部</button>
          </div>
        </div>

        <!-- 班级筛选 -->
        <div class="filter-group">
          <label class="filter-label">班级：</label>
          <div class="class-selector">
            <select class="class-dropdown">
              <option value="all">全部班级</option>
              <option value="1-1">初一(1)班</option>
              <option value="1-2">初一(2)班</option>
              <option value="1-3">初一(3)班</option>
              <option value="2-1">初二(1)班</option>
              <option value="2-2">初二(2)班</option>
              <option value="2-3">初二(3)班</option>
              <option value="3-1">初三(1)班</option>
              <option value="3-2">初三(2)班</option>
              <option value="3-3">初三(3)班</option>
            </select>
          </div>
        </div>

        <!-- 搜索框 -->
        <div class="filter-group search-group">
          <div class="search-container">
            <input type="text" placeholder="搜索学生姓名或学号" class="search-input" />
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 学生列表区域 -->
    <div class="student-table-container">
      <table class="student-table">
        <!-- 表头 -->
        <thead>
          <tr class="table-header">
            <th class="table-checkbox">
              <input type="checkbox" class="header-checkbox" />
            </th>
            <th>学号</th>
            <th>姓名</th>
            <th>年级</th>
            <th>班级</th>
            <th>性别</th>
            <th>出生日期</th>
            <th>操作</th>
          </tr>
        </thead>
        <!-- 表体 -->
        <tbody>
          <!-- 示例数据行，实际使用时将由数据驱动 -->
          <tr class="table-row" v-for="(student,index) in students" :key="index">
            <td class="table-checkbox">
              <input type="checkbox" class="row-checkbox" />
            </td>
            <td>{{student.username}}</td>
            <td>{{student.name}}</td>
            <td>初一</td>
            <td>初一(1)班</td>
            <td>男</td>
            <td>2010-09-15</td>
            <td class="action-buttons">
              <button class="btn-view">查看</button>
              <button class="btn-edit">编辑</button>
              <button class="btn-delete">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 分页区域 -->
    <div class="pagination-section">
      <div class="pagination-info">
        共 <span class="total-count">{{count}}</span> 条记录，当前第 <span class="current-page">{{ page }}</span> 页，共 <span class="total-pages">{{ page_count }}</span> 页
      </div>
      <div class="pagination-controls">
        <button class="page-btn">首页</button>
        <!--  page-btn page-btn-active  //  page-btn     -->
        <button class="page-btn page-btn-disabled">上一页</button>
        <button v-for="index in page_count" :key="index" :class="changePage(index)" @click="getStudents(index)">{{ index }}</button>
        <button class="page-btn">下一页</button>
        <button class="page-btn">尾页</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.student-management {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 标题样式 */
.management-header {
  margin-bottom: 24px;
}

.management-header h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}

/* 筛选区域样式 */
.filter-section {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}

.filter-controls {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-label {
  font-size: 14px;
  color: #4b5563;
  font-weight: 500;
  white-space: nowrap;
}

/* 年级按钮样式 */
.grade-buttons {
  display: flex;
  gap: 8px;
}

.grade-btn {
  padding: 6px 16px;
  border: 1px solid #d1d5db;
  background-color: #ffffff;
  border-radius: 4px;
  font-size: 14px;
  color: #6b7280;
  cursor: pointer;
  transition: all 0.2s ease;
}

.grade-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.grade-btn-active {
  background-color: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
}

.grade-btn-all {
  background-color: #f3f4f6;
  font-weight: 500;
}

/* 班级选择器样式 */
.class-dropdown {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
  color: #374151;
  background-color: #ffffff;
  cursor: pointer;
  transition: border-color 0.2s ease;
  min-width: 120px;
}

.class-dropdown:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 搜索框样式 */
.search-group {
  margin-left: auto;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  padding: 8px 40px 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
  color: #374151;
  width: 300px;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  position: absolute;
  right: 12px;
  color: #9ca3af;
  pointer-events: none;
}

/* 学生表格样式 */
.student-table-container {
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.table-header {
  background-color: #f9fafb;
  border-bottom: 2px solid #e5e7eb;
}

.table-header th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.table-header th:last-child {
  text-align: center;
}

.table-row {
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.2s ease;
}

.table-row:hover {
  background-color: #f9fafb;
}

.table-row td {
  padding: 12px 16px;
  color: #374151;
}

.table-row td:last-child {
  text-align: center;
}

/* 复选框样式 */
.table-checkbox {
  width: 40px;
}

.header-checkbox,
.row-checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.btn-view,
.btn-edit,
.btn-delete {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
}

.btn-view {
  background-color: #f3f4f6;
  color: #4b5563;
}

.btn-view:hover {
  background-color: #e5e7eb;
}

.btn-edit {
  background-color: #dbeafe;
  color: #1e40af;
}

.btn-edit:hover {
  background-color: #bfdbfe;
}

.btn-delete {
  background-color: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background-color: #fecaca;
}

/* 分页样式 */
.pagination-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 16px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}

.pagination-info {
  font-size: 14px;
  color: #6b7280;
}

.total-count,
.current-page,
.total-pages {
  color: #374151;
  font-weight: 500;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  background-color: #ffffff;
  border-radius: 4px;
  font-size: 14px;
  color: #374151;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn:hover:not(.page-btn-disabled) {
  border-color: #3b82f6;
  color: #3b82f6;
}

.page-btn-active {
  background-color: #3b82f6;
  border-color: #3b82f6;
  color: #ffffff;
}

.page-btn-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-ellipsis {
  padding: 0 4px;
  color: #6b7280;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .search-input {
    width: 240px;
  }
}

@media (max-width: 992px) {
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .search-group {
    margin-left: 0;
  }
  
  .search-input {
    width: 100%;
  }
  
  .pagination-section {
    flex-direction: column;
    gap: 16px;
    align-items: center;
  }
  
  /* 表格滚动 */
  .student-table-container {
    overflow-x: auto;
  }
  
  .student-table {
    min-width: 768px;
  }
}

@media (max-width: 768px) {
  .student-management {
    padding: 16px;
  }
  
  .grade-buttons {
    flex-wrap: wrap;
  }
  
  .management-header h2 {
    font-size: 20px;
  }
}
</style>
