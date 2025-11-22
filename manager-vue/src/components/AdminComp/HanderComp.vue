<script>
export default {
  name: 'HanderComp',
  data() {
    return {
      name: null,
      dropdownVisible: false
    }
  },
  created() {
    document.addEventListener('click', this.handleClickOutside)
    // 获取登入信息
    if(sessionStorage.getItem('name')){this.name = sessionStorage.getItem('name')}
    if(localStorage.getItem('name')){this.name = localStorage.getItem('name')}
    if (this.name === null) {
      this.$message.error('请先登录')
      this.$router.push('/')
    }
  },
  methods: {
    // 切换下拉框显示
    toggleDropdown() {
      this.dropdownVisible = !this.dropdownVisible
    },
    // 退出登录
    logout() {
      // 清除本地存储的用户信息
      localStorage.clear()
      sessionStorage.clear()
      // 显示退出成功提示
      this.$message.success('退出登录成功')
      // 跳转到登录页面
      this.$router.push('/')
    },
    // 点击外部关闭下拉框
    handleClickOutside() {
      this.dropdownVisible = false
    }
  },
  beforeDestroy() {
    document.removeEventListener('click', this.handleClickOutside)
  }
}
</script>

<template>
  <div class="header-container">
    <div class="nav-bar">
      <!-- 左侧标题 -->
      <div class="nav-title">学生宿舍管理系统</div>
      
      <!-- 中间导航选项 -->
      <div class="nav-options">
        <router-link to="/dashboard" class="nav-item">首页</router-link>
        <router-link to="/student" class="nav-item">学生管理</router-link>
        <router-link to="/dorm" class="nav-item">宿舍管理</router-link>
        <router-link to="/repair" class="nav-item">维修申请</router-link>
        <router-link to="/notice" class="nav-item">公告管理</router-link>
      </div>
      
      <!-- 右侧用户信息 -->
      <div class="user-info" @click.stop="toggleDropdown">
        <el-avatar :size="32" icon="el-icon-user"></el-avatar>
        <span class="username">管理员：{{ name }}</span>
        <i :class="['el-icon-caret-bottom', { 'rotate-180': dropdownVisible }]"></i>
        
        <!-- 下拉菜单 -->
        <div class="dropdown-menu" v-if="dropdownVisible">
          <div class="dropdown-item">
            <i class="el-icon-user"></i>
            <span>个人信息</span>
          </div>
          <div class="dropdown-item">
            <i class="el-icon-setting"></i>
            <span>系统设置</span>
          </div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-item logout" @click="logout">
            <i class="el-icon-switch-button"></i>
            <span>退出登录</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 全局过渡动画 */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* 主容器 */
.header-container {
  width: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.nav-bar {
  display: flex;
  align-items: center;
  padding: 0 40px;
  height: 64px;
  max-width: 1440px;
  margin: 0 auto;
}

/* 左侧标题 */
.nav-title {
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
  margin-right: 80px;
  letter-spacing: 1px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.nav-title:hover {
  transform: scale(1.05);
}

/* 中间导航选项 */
.nav-options {
  display: flex;
  flex: 1;
  gap: 10px;
}

.nav-item {
  padding: 0 24px;
  height: 64px;
  line-height: 64px;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  border-radius: 8px;
  margin: 0 4px;
}

.nav-item:hover {
  color: #ffffff;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.nav-item.router-link-active {
  color: #ffffff;
  background-color: rgba(255, 255, 255, 0.15);
}

.nav-item.router-link-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 20%;
  right: 20%;
  height: 3px;
  background-color: #ffffff;
  border-radius: 3px;
  animation: fadeIn 0.3s ease;
}

/* 右侧用户信息 */
.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 25px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.user-info:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.username {
  margin: 0 8px;
  font-size: 14px;
  font-weight: 500;
  color: #ffffff;
}

.el-icon-caret-bottom {
  transition: transform 0.3s ease;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

.rotate-180 {
  transform: rotate(180deg);
}

/* 下拉菜单 */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  min-width: 180px;
  background-color: #ffffff;
  border: none;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  overflow: hidden;
  animation: slideDown 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 14px 24px;
  font-size: 14px;
  color: #303133;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.dropdown-item::before {
  content: '';
  position: absolute;
  left: -40px;
  top: 0;
  width: 30px;
  height: 100%;
  background-color: rgba(102, 126, 234, 0.1);
  transform: skewX(-20deg);
  transition: all 0.3s ease;
}

.dropdown-item:hover::before {
  left: 100%;
}

.dropdown-item:hover {
  background-color: #f8f9ff;
  color: #667eea;
  padding-left: 28px;
}

.dropdown-item i {
  margin-right: 12px;
  font-size: 18px;
  width: 18px;
  text-align: center;
  transition: transform 0.3s ease;
}

.dropdown-item:hover i {
  transform: scale(1.2);
}

.dropdown-divider {
  height: 1px;
  background-color: #f0f0f0;
  margin: 4px 0;
}

/* 退出登录特殊样式 */
.dropdown-item.logout {
  color: #f56c6c;
  font-weight: 500;
}

.dropdown-item.logout:hover {
  background-color: #fff0f0;
  color: #f56c6c;
}

.dropdown-item.logout:hover::before {
  background-color: rgba(245, 108, 108, 0.1);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .nav-bar {
    padding: 0 20px;
  }
  
  .nav-title {
    font-size: 18px;
    margin-right: 30px;
  }
  
  .nav-item {
    padding: 0 16px;
    font-size: 14px;
  }
  
  .user-info {
    padding: 6px 12px;
  }
  
  .username {
    font-size: 12px;
  }
}
</style>