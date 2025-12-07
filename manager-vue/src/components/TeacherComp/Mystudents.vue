<script>
export default {
  name: 'MyStudents',
  data() {
    return {
      students: [],                        // 学生列表数据
      loading: false,                      // 加载状态
      searchParams: {
        search: '',                        // 搜索关键词（学号或宿舍号）
        gender: ''                         // 性别过滤
      },
      token: '',                           // 访问令牌
      refreshToken: ''                     // 刷新令牌
    }
  },
  mounted() {
    // 从settings.js获取令牌
    this.token = this.$settings.getToken()
    this.refreshToken = this.$settings.getRefreshToken()
    // 页面挂载时获取学生列表
    this.getStudents()
  },
  methods: {
    // 获取学生列表
    async getStudents() {
      this.loading = true
      try {
        // 构建请求URL，添加查询参数
        let url = `${this.$settings.Host}/teacher/get/allStudents/`
        let queryParams = []
        
        if (this.searchParams.search) {
          queryParams.push(`search=${encodeURIComponent(this.searchParams.search)}`)
        }
        if (this.searchParams.gender) {
          queryParams.push(`gender=${encodeURIComponent(this.searchParams.gender)}`)
        }
        
        if (queryParams.length > 0) {
          url += '?' + queryParams.join('&')
        }
        
        // 发送请求获取学生列表
        const response = await this.$axios.get(url, {
          headers: {
            'Authorization': `Hander ${this.token}`
          }
        })
        
        this.students = response.data
      } catch (error) {
        console.error('获取学生列表失败:', error)
        
        // 如果是401错误，尝试刷新令牌
        if (error.response && error.response.status === 401) {
          await this.refreshTokenFunc()
        } else {
          alert('获取学生列表失败，请稍后重试')
        }
      } finally {
        this.loading = false
      }
    },
    
    // 刷新令牌
    async refreshTokenFunc() {
      try {
        const response = await this.$axios.post(`${this.$settings.Host}/users/refresh/`, {
          refresh: this.refreshToken
        })
        
        // 更新令牌
        this.token = response.data.access
        this.refreshToken = response.data.refresh || this.refreshToken
        
        // 保存到本地存储
        localStorage.setItem('token', this.token)
        sessionStorage.setItem('token', this.token)
        if (response.data.refresh) {
          localStorage.setItem('refresh_token', this.refreshToken)
          sessionStorage.setItem('refresh_token', this.refreshToken)
        }
        // 重新获取学生列表
        this.getStudents()
      } catch (error) {
        console.error('刷新令牌失败:', error)
        alert('令牌已过期，请重新登录')
        this.$router.push({name: 'Login'})
      }
    },
    
    // 处理搜索和过滤
    handleSearch() {
      this.getStudents()
    }
  },
}
</script>

<template>
  <div class="student-container">
    <!-- 标题区域 -->
    <div class="page-header">
      <h1 class="page-title">我的学生</h1>
      <p class="page-subtitle">管理和查看我负责的学生信息</p>
    </div>
    
    <!-- 搜索和过滤区域 -->
    <div class="search-filter">
      <input 
        type="text" 
        v-model="searchParams.search"
        placeholder="搜索学号或宿舍号"
        class="search-input"
      />
      <select v-model="searchParams.gender" @change="getStudents" class="filter-select">
        <option value="">全部性别</option>
        <option value="male">男</option>
        <option value="female">女</option>
      </select>
      <button @click="handleSearch" class="search-btn">搜索</button>
    </div>
    
    <!-- 学生列表表格 -->
    <div class="student-table-container">
      <table class="student-table" v-if="!loading">
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
            <td>{{ student.house_number }}</td>
          </tr>
          <tr v-if="students.length === 0">
            <td colspan="4" class="empty-data">暂无学生数据</td>
          </tr>
        </tbody>
      </table>
      <div class="loading" v-if="loading">加载中...</div>
    </div>
  </div>
</template>

<style>
/* 全局背景色设置 */
html, body {
  margin: 0;
  padding: 0;
  background-color: #f8f9fa;
}
</style>

<style scoped>
/* 容器样式 */
.student-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px;
  min-height: 100vh;
}

/* 标题区域 */
.page-header {
  margin-bottom: 3rem;
  color: #1e293b;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 8px 0;
  letter-spacing: 0.5px;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.page-subtitle {
  font-size: 16px;
  color: #909399;
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

/* 搜索过滤区域 */
.search-filter {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
  padding: 24px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
  align-items: center;
}

.search-input, .filter-select {
  padding: 12px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background-color: white;
  color: #303133;
}

.search-input:focus, .filter-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

.search-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}

.search-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.search-btn:active {
  transform: translateY(0);
}

/* 学生列表表格 */
.student-table-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
  overflow: hidden;
}

.student-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
}

.student-table th, .student-table td {
  padding: 16px 20px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
  font-size: 14px;
}

.student-table th {
  background-color: #f5f7fa;
  font-weight: 600;
  color: #606266;
  white-space: nowrap;
}

.student-table td {
  color: #303133;
}

.student-table tr {
  transition: all 0.3s ease;
}

.student-table tr:hover {
  background-color: rgba(102, 126, 234, 0.05);
}

.student-table tr:last-child td {
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

/* 加载状态 */
.loading {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
  color: #667eea;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
}

/* 无数据状态 */
.empty-data {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
  color: #909399;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .student-container {
    padding: 16px;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
  }
  
  .search-filter {
    flex-direction: column;
    padding: 16px;
  }
  
  .search-input, .filter-select, .search-btn {
    width: 100%;
  }
  
  .student-table-container {
    overflow-x: auto;
  }
  
  .student-table {
    min-width: 600px;
  }
  
  .student-table th, .student-table td {
    padding: 12px 16px;
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .student-container {
    padding: 8px;
  }
  
  .page-title {
    font-size: 1.75rem;
  }
  
  .page-header {
    margin-bottom: 24px;
  }
  
  .search-filter {
    gap: 12px;
    padding: 12px;
  }
  
  .student-table th, .student-table td {
    padding: 10px 12px;
  }
}
</style>