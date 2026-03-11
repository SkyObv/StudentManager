<script>
// 老师导航栏组件
export default {
  name: 'HeaderComp',
  data() {
    return {
      option:0,                                                      // 选择标志
      name:'',                                                       // 用户名
      first_name:'',                                                 // 性
      user_type:'',                                                  // 用户类型
      token:'',                                                      // 登入令牌
      refresh:'',                                                    // 刷新令牌
    }
  },
  created() {
    this.getUser()
  },
  methods:{
    // 导航状态切换函数
    changeOption(option){this.option = option;this.$emit('update-option', this.option);},
    changeCss(option){if (option === this.option){return "nav-item active"}else {return "nav-item"}},
    // 获取登入信息
    getUser(){
      this.name = localStorage.getItem('name') || sessionStorage.getItem('name')
      this.first_name = this.name.charAt(0)
      this.user_type = localStorage.getItem('user_type') || sessionStorage.getItem('user_type')
      this.token = localStorage.getItem('token') || sessionStorage.getItem('token')
      this.refresh = localStorage.getItem('refresh') || sessionStorage.getItem('refresh')
      if (!this.token){
        this.$message.error("请先登入！")
        this.$router.push({name: 'Login'})
      }
    },
    // 退出登入
    quit(){
      localStorage.clear();
      sessionStorage.clear();
      this.$router.push({name: 'Login'})
      this.$message.success("退出成功！")
    }
  }
}
</script>
<template>
  <header class="header-container">
    <div class="header-content">
      <!-- 左侧Logo和标题 -->
      <div class="logo-section">
        <div class="logo-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
          </svg>
        </div>
        <h1 class="logo-title">学生宿舍管理控制系统</h1>
      </div>

      <!-- 中间导航菜单 -->
      <nav class="main-nav">
        <ul class="nav-menu">
          <li :class="changeCss(0)" @click="changeOption(0)">
            <a href="#dorm-application" class="nav-link">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
              </svg>
              <span>宿舍申请</span>
            </a>
          </li>
          <li :class="changeCss(1)" @click="changeOption(1)">
            <a href="#application-records" class="nav-link">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
              </svg>
              <span>申请记录</span>
            </a>
          </li>
          <li :class="changeCss(2)" @click="changeOption(2)">
            <a href="#my-dorm" class="nav-link">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9 22 9 12 15 12 15 22"></polyline>
              </svg>
              <span>我的宿舍</span>
            </a>
          </li>
          <li :class="changeCss(3)" @click="changeOption(3)">
            <a href="#my-students" class="nav-link">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
              <span>我的学生</span>
            </a>
          </li>
          <li :class="changeCss(4)" @click="changeOption(4)">
            <a href="#dorm-allocation" class="nav-link">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 3v18h18"></path>
                <path d="M9 9h6v6"></path>
                <path d="M9 15v-6"></path>
                <path d="M15 9h-6v6"></path>
                <path d="M3 9h18"></path>
                <path d="M3 15h18"></path>
              </svg>
              <span>门禁卡管理</span>
            </a>
          </li>
        </ul>
      </nav>

      <!-- 右侧用户信息区域 -->
      <div class="user-section">
        <!-- 通知图标 -->
        <div class="notification-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <span class="notification-badge">3</span>
        </div>

        <!-- 用户头像和下拉菜单 -->
        <div class="user-dropdown">
          <div class="user-info">
            <div class="avatar">
              <span class="avatar-text">{{ first_name }}</span>
            </div>
            <div class="user-details">
              <div class="username">{{ name }}</div>
              <div class="user-role">{{ user_type }}</div>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>

          <!-- 下拉菜单内容 -->
          <div class="dropdown-content">
            <a href="#logout" class="dropdown-item logout">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                <polyline points="16 17 21 12 16 7"></polyline>
                <line x1="21" y1="12" x2="9" y2="12"></line>
              </svg>
              <span @click="quit">退出登录</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* 导航栏容器 */
.header-container {
  position: sticky;
  top: 0;
  left: 0;
  width: 100%;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  z-index: 1000;
  transition: all 0.3s ease;
}

/* 导航栏内容区 */
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  padding: 0 32px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 左侧Logo区域 */
.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.logo-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  letter-spacing: 0.5px;
}

/* 中间导航菜单 */
.main-nav {
  flex: 1;
  display: flex;
  justify-content: center;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 24px;
  margin: 0;
  padding: 0;
}

.nav-item {
  position: relative;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  color: #606266;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-size: 15px;
  font-weight: 500;
}

.nav-link:hover {
  color: #667eea;
  background-color: rgba(102, 126, 234, 0.1);
}

.nav-item.active .nav-link {
  color: #667eea;
  background-color: rgba(102, 126, 234, 0.15);
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 16px;
  right: 16px;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 3px;
}

/* 右侧用户区域 */
.user-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 通知图标 */
.notification-icon {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s ease;
}

.notification-icon:hover {
  background-color: #f5f7fa;
  color: #667eea;
}

.notification-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  min-width: 18px;
  height: 18px;
  padding: 0 6px;
  background-color: #f56c6c;
  color: white;
  font-size: 12px;
  font-weight: 600;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 用户下拉菜单 */
.user-dropdown {
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-info:hover {
  background-color: #f5f7fa;
}

/* 头像样式 */
.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 15px;
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.username {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

.user-role {
  font-size: 12px;
  color: #909399;
}

/* 下拉菜单内容 */
.dropdown-content {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 200px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  opacity: 0;
  visibility: hidden;
  transform: translateY(8px);
  transition: all 0.3s ease;
  z-index: 1001;
}

.user-dropdown:hover .dropdown-content {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: #606266;
  text-decoration: none;
  transition: all 0.2s ease;
  font-size: 14px;
}

.dropdown-item:hover {
  background-color: #f5f7fa;
  color: #667eea;
}

.dropdown-divider {
  height: 1px;
  background-color: #ebeef5;
  margin: 4px 0;
}

.dropdown-item.logout {
  color: #f56c6c;
}

.dropdown-item.logout:hover {
  background-color: #fef0f0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .header-content {
    padding: 0 24px;
  }
  
  .nav-menu {
    gap: 16px;
  }
  
  .nav-link {
    padding: 8px 12px;
    font-size: 14px;
  }
}

@media (max-width: 992px) {
  .main-nav {
    display: none;
  }
  
  .header-content {
    padding: 0 20px;
  }
}

/* 平滑过渡动画 */
.header-container,
.logo-icon,
.nav-link,
.user-info,
.dropdown-content,
.dropdown-item {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 微交互效果 */
.nav-link:active,
.dropdown-item:active {
  transform: scale(0.98);
}

/* 滚动时的导航栏样式 */
.header-container.scrolled {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  height: 60px;
}

.header-container.scrolled .header-content {
  height: 60px;
}
</style>