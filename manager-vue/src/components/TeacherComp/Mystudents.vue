<script>
// 我的学生页面
import StudentsTable from '@/components/publicComp/StudentsTable.vue'
export default {
  name: 'MyStudents',
  data() {
    return {
      MyStudents: [],                                                // 我的学生
      studentFile: null,                                             // 学生文件
      showUpdateDialog: false,                                       // 是否显示更新弹窗
    }
  },
  components:{
    StudentsTable,
  },
  
  created() {
    this.getMyStudents();                                            // 获取我的学生
  },
  methods: {
    getMyStudents() {                                                // 获取我的学生
      this.$axios({
        url: `${this.$settings.Host}/teacher/get/allStudents/`,
        method: 'get',
        params: {},                                                 // 显式指定params为空对象
        headers: {
          'Authorization': `Hander ${this.$settings.getToken()}`
        },
        data: {}
      }).then(res => {
        console.log(res.data);
        this.MyStudents = res.data;
      }).catch(err => {
        this.$message.error('获取我的学生失败');
        console.error(err);
      })
    },
    
    closeDialog() {                                                  // 关闭弹窗
      this.showUpdateDialog = false;
    },
    handleFileChange(event) {                                        // 处理文件选择
      const file = event.target.files[0];
      if (file) {
        this.studentFile = file;
      }
    },
    removeFile() {                                                   // 删除选中的文件
      this.studentFile = null;
      this.$refs.fileInput.value = '';
    },
    selectFile() {                                                   // 选择文件
      if (!this.studentFile) {
        this.$message.warning('请先选择文件');
        return;
      }
      
      this.$message.success(`已选择文件: ${this.studentFile.name}`);
      this.closeDialog();
    },
    executeUpdate() {                                                // 执行更新操作
      // 使用console.log模拟请求
      console.log('===== 开始模拟更新学生数据请求 =====');
      console.log('文件名:', this.studentFile.name);
      console.log('文件大小:', this.studentFile.size);
      console.log('文件类型:', this.studentFile.type);
      console.log('最后修改时间:', new Date(this.studentFile.lastModified));
      // 重置文件
      this.removeFile();
    },
  },
}
</script>

<template>
  <div class="student-container">
    <!-- 标题区域 -->
    <div class="page-header">
      <h1 class="page-title">我的学生</h1>
      <p class="page-subtitle">查看我负责的学生信息</p>
    </div>
    
    <!-- 功能按钮区域 -->
    <div class="action-container">
      <button class="action-button" @click="showUpdateDialog = true">
        <span class="button-icon">🔄</span>
        更新我的学生
      </button>
      <button class="execute-button" v-if="studentFile" @click="executeUpdate">
        <span class="button-icon">⚡</span>
        执行更新
      </button>
    </div>
    
    <!-- 学生列表表格 -->
    <div class="table-container">
      <StudentsTable 
      :students="MyStudents"
      ></StudentsTable>
    </div>
    
    <!-- 更新学生弹窗 -->
    <div class="dialog-overlay" v-if="showUpdateDialog" @click="closeDialog">
      <div class="dialog-content" @click.stop>
        <div class="dialog-header">
          <h3>更新学生数据</h3>
          <button class="close-button" @click="closeDialog">×</button>
        </div>
        <div class="dialog-body">
          <p class="warning-text">当前操作会删除现有的所有学生，同时会添加所选文件中的所有学生</p>
          
          <div class="file-upload-area" v-if="!studentFile">
            <button class="file-select-button" @click="$refs.fileInput.click()">
              选择文件
            </button>
            <input 
              type="file" 
              ref="fileInput" 
              accept=".xlsx" 
              style="display: none" 
              @change="handleFileChange"
            >
          </div>
          
          <div class="selected-file" v-else>
            <span class="file-icon">📄</span>
            <span class="file-name">{{ studentFile.name }}</span>
            <button class="remove-file" @click="removeFile" title="删除文件">×</button>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="cancel-button" @click="closeDialog">取消</button>
          <button class="confirm-button" @click="selectFile" :disabled="!studentFile">选择文件</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面容器 */
.student-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 标题区域 */
.page-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 3rem;
  color: #1e293b;
  animation: fadeInDown 0.6s ease-out;
  width: 100%;
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
  animation: slideInUp 0.8s ease-out 0.2s both;
  text-align: center;
  width: 100%;
}

.page-subtitle {
  font-size: 16px;
  color: #909399;
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  animation: fadeIn 1s ease-out 0.4s both;
}

/* 功能按钮区域 */
.action-container {
  max-width: 1200px;
  margin: 0 auto 2rem;
  padding: 0 24px;
  display: flex;
  justify-content: flex-end;
  animation: fadeIn 0.8s ease-out 0.6s both;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.execute-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #f56565 0%, #ed64a6 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(245, 101, 101, 0.3);
  margin-left: 12px;
}

.execute-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 101, 101, 0.4);
}

.button-icon {
  font-size: 16px;
}

/* 表格容器 */
.table-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  animation: fadeIn 0.8s ease-out 0.8s both;
}

/* 弹窗样式 */
.dialog-overlay {
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
}

.dialog-content {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: slideInUp 0.3s ease-out;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 0;
  border-bottom: 1px solid #ebeef5;
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #909399;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  color: #606266;
}

.dialog-body {
  padding: 24px;
}

.warning-text {
  margin: 0 0 20px;
  color: #e6a23c;
  font-size: 14px;
  line-height: 1.5;
}

.file-upload-area {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.file-select-button {
  padding: 10px 20px;
  background-color: #f5f7fa;
  color: #606266;
  border: 1px dashed #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.file-select-button:hover {
  border-color: #667eea;
  color: #667eea;
}

.selected-file {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background-color: #f5f7fa;
  border-radius: 6px;
  margin: 20px 0;
}

.file-icon {
  font-size: 20px;
}

.file-name {
  flex: 1;
  font-size: 14px;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.remove-file {
  background: none;
  border: none;
  color: #f56c6c;
  cursor: pointer;
  font-size: 18px;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s;
}

.remove-file:hover {
  background-color: #fef0f0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 0 24px 24px;
}

.cancel-button, .confirm-button {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-button {
  background-color: #f5f7fa;
  color: #606266;
  border: 1px solid #dcdfe6;
}

.cancel-button:hover {
  color: #667eea;
  border-color: #667eea;
}

.confirm-button {
  background-color: #667eea;
  color: white;
  border: 1px solid #667eea;
}

.confirm-button:hover {
  background-color: #5a6fd8;
}

.confirm-button:disabled {
  background-color: #c0c4cc;
  border-color: #c0c4cc;
  cursor: not-allowed;
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

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>