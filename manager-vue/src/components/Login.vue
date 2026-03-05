<script>
/* eslint-disable vue/multi-word-component-names */
export default {
  name:"Login",
  data() {
    return {
      identity: '',                                                  // 用户类型：student, teacher, admins
      loginForm:{                                                    // 登入表单
        username: '',
        password: '',
      },
      rememberMe: false,                                             // 记住我选项
      // 表单验证规则
      rules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' },
          { min: 1, message: '账号不能为空', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 1, message: '密码不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    sessionStorage.clear();
    localStorage.clear();
  },
  methods: {
    // 登入
    Login(){
      // 检查是否选择了用户类型
      if (!this.identity) {
        this.$message.warning('请选择用户类型')
        return
      }
      this.$axios.post(`${this.$settings.Host}/users/login/`,
          {'username':this.loginForm.username, 'password':this.loginForm.password, 'user_type':this.identity}).then(response => {
        if (this.rememberMe){
          localStorage.token = response.data.access
          localStorage.refresh = response.data.refresh
          localStorage.user_type = response.data.user_type
          localStorage.name = response.data.name
        }
        else {
          sessionStorage.token = response.data.access
          sessionStorage.refresh = response.data.refresh
          sessionStorage.user_type = response.data.user_type
          sessionStorage.name = response.data.name
        }
        // 学生页面
        this.$message.success("登入成功")
        if (response.data.user_type === 'student'){
          this.$router.push({name: 'StudentComp'})
        }
        // 管理者页面
        if (response.data.user_type ==='admin'){
          this.$router.push({name: 'AdminComp'})
        }
        // 老师页面
        if (response.data.user_type === 'teacher'){
          this.$router.push({name: 'TeacherComp'})
        }
      }).catch(error => {
        console.log(error)
        this.$message.error("用户名、密码或角色不匹配")
      })
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
        <el-radio-group v-model="identity" size="medium">
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
          <el-checkbox v-model="rememberMe" class="remember-me">记住我</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button 
            type="primary" 
            class="login-button" 
            size="medium"
            @click="Login"
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

.remember-me {
  text-align: left;
  margin-bottom: 20px;
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #667eea;
  border-color: #667eea;
}

:deep(.el-checkbox__inner:hover) {
  border-color: #667eea;
}
</style>