<script>
/* eslint-disable vue/multi-word-component-names */

export default {
  name:"Login",
  data() {
    return {
      userType: 'student',                                           // 用户类型：student, teacher, admin
      loginForm:{                                                    // 登入表单
        username: '',
        password: '',
      },
      // 表单验证规则
      rules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 1, message: '账号不能为空', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 8, message: '密码不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleLogin(){
      console.log('登录')
      console.log(this.loginForm + " " + this.userType)
    }
  }
}
</script>

<template>
  <div class="login-container">
    <!-- 背景视频 -->
    <video class="bg-video" autoplay muted loop playsinline>
      <source src="/staticVoid/登入背景视频.mp4" type="video/mp4">
    </video>
    <div class="video-overlay"></div>
    
    <div class="login-form-wrapper">
      <h2 class="login-title">统一登录系统</h2>
      
      <!-- 用户类型选择 -->
      <div class="user-type-section">
        <el-radio-group v-model="userType" size="medium">
          <el-radio-button label="student">学生</el-radio-button>
          <el-radio-button label="teacher">教师</el-radio-button>
          <el-radio-button label="admin">管理者</el-radio-button>
        </el-radio-group>
      </div>
      <!-- 登录表单 -->
      <el-form :model="loginForm" class="login-form" :rules="rules" ref="loginFormRef">
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            placeholder="请输入账号" 
            prefix-icon="el-icon-user" 
            size="medium"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="请输入密码" 
            prefix-icon="el-icon-lock" 
            size="medium"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            class="login-button" 
            size="medium"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* 背景视频样式 */
.bg-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}

/* 视频遮罩层，增强文字可读性 */
.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.login-form-wrapper {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 40px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
  position: relative;
  z-index: 2;
}

.login-form-wrapper:hover {
  transform: translateY(-5px);
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.user-type-section {
  margin-bottom: 30px;
}

.login-form {
  width: 100%;
}

.login-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

:deep(.el-radio-button__orig-radio:checked+.el-radio-button__inner) {
  background-color: #667eea;
  border-color: #667eea;
}

:deep(.el-radio-button__orig-radio:checked+.el-radio-button__inner:hover) {
  background-color: #5a6bda;
  border-color: #5a6bda;
}

:deep(.el-button--primary) {
  background-color: #667eea;
  border-color: #667eea;
}

:deep(.el-button--primary:hover) {
  background-color: #5a6bda;
  border-color: #5a6bda;
}

:deep(.el-input__inner:focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}
</style>