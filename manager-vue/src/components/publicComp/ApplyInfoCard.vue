<script>
// 宿舍申请记录卡片

import settings from "@/settings";

export default {
  name: 'ApplyInfoCard',
  // 父组件向子组件传递的数据
  props: {
    // 卡片数据
    applyInfo: {
      type: Object,
      required: true,
    },
    // 是否显示操作按钮
    showActionButtons: {
      type: Boolean,
      default:false
    }
  },
  methods: {
    // 根据申请状态返回对应的CSS类名
    getStateClass(state) {
      switch (state) {
        case '待审核':
          return 'state-pending';
        case '通过':
          return 'state-approved';
        case '拒绝':
          return 'state-rejected';
        default:
          return '';
      }
    },
    // 格式化申请时间
    formatApplyTime(timeStr) {
      if (!timeStr) return '';
      const date = new Date(timeStr);
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
    },
    // 处理同意按钮点击
    async handleApprove() {
      var apply_id = this.applyInfo.id;         // 获取当前申请的ID
      const token = settings.getToken();        // 获取token
      // 构建请求URL
      const url = `${settings.Host}/teacher/apply/upadte/${apply_id}/`;
      // 准备请求头
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Hander ${token}`
      };
      // 准备请求体
      const data = {
        "apply_state": "通过"
      };
      try {
        // 发送PATCH请求
        const response = await fetch(url, {
          method: 'PATCH',
          headers: headers,
          body: JSON.stringify(data)
        });
        // 检查响应状态
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.$message.success('同意申请成功');
        this.$emit('refresh');
      } catch (error) {
        this.$message.error('同意申请失败，请重试');
      }
    },
    // 处理拒绝按钮点击
    async handleReject() {
      var apply_id = this.applyInfo.id;         // 获取当前申请的ID
      const token = settings.getToken();        // 获取token
      // 构建请求URL
      const url = `${settings.Host}/teacher/apply/upadte/${apply_id}/`;
      // 准备请求头
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Hander ${token}`
      };
      // 准备请求体
      const data = {
        "apply_state": "拒绝"
      };
      try {
        // 发送PATCH请求
        const response = await fetch(url, {
          method: 'PATCH',
          headers: headers,
          body: JSON.stringify(data)
        });
        // 检查响应状态
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.$message.success('拒绝申请成功');
        this.$emit('refresh');
      } catch (error) {
        this.$message.error('拒绝申请失败，请重试');
      }
    },
    // 处理已读/删除/撤销按钮点击
    async handleReadDelete() {
      var apply_id = this.applyInfo.id;         // 获取当前申请的ID
      const token = settings.getToken();        // 获取token
      
      // 检查令牌是否存在
      if (!token) {
        this.$message.error('请先登录获取令牌');
        return;
      }
      
      // 构建请求URL
      const url = `${settings.Host}/teacher/apply/delete/${apply_id}/`;
      // 准备请求头
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Hander ${token}`
      };
      try {
        // 发送DELETE请求
        const response = await fetch(url, {
          method: 'DELETE',
          headers: headers,
        });
        // 检查响应状态
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        this.$message.success('删除成功');
        this.$emit('refresh');
      } catch (error) {
        console.error('删除失败:', error);
        this.$message.error('删除失败，请重试');
      }
    }
  }
}
</script>

<template>
  <div class="apply-info-card">
    <div class="card-header">
      <div class="header-main">
        <div class="header-content">
          <h3 class="teacher-name">{{ applyInfo.teacher_name }}</h3>
          <div class="apply-state" :class="getStateClass(applyInfo.apply_state || '待审核')">{{ applyInfo.apply_state || '待审核' }}</div>
        </div>
      </div>
      <!-- 已读/删除/撤销按钮，始终显示在右上角 -->
      <template v-if="!showActionButtons">
        <button class="read-delete-button" @click="handleReadDelete">
        已读删除或撤销
        </button>
      </template>
    </div>
    <div class="card-body">
      <div class="card-content">
        <div class="info-item">
          <span class="info-label">宿舍名称：</span>
          <span class="info-value">{{ applyInfo.hostel_name }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">申请时间：</span>
          <span class="info-value">{{ formatApplyTime(applyInfo.apply_time) }}</span>
        </div>
      </div>
      
      <!-- 操作按钮区域 -->
    <div class="card-actions">
      <!-- 同意和拒绝按钮，根据showActionButtons控制显示 -->
      <template v-if="showActionButtons">
        <button class="action-button approve-button" @click="handleApprove">
          同意
        </button>
        <button class="action-button reject-button" @click="handleReject">
          拒绝
        </button>
      </template>
    </div>
    </div>
  </div>
</template>

<style scoped>
.apply-info-card {
  width: 100%;
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.12);
  padding: 24px 32px;
  margin-bottom: 24px;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.apply-info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

/* 状态徽章样式 */
.status-badge {
  position: absolute;
  top: 16px;
  right: 120px;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  z-index: 15;
  transition: all 0.3s ease;
}

.status-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.apply-info-card:hover {
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12), 0 4px 12px rgba(0, 0, 0, 0.16);
  transform: translateY(-4px) scale(1.01);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  position: relative;
  gap: 8px;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-grow: 1;
  overflow: hidden;
}

.header-content {
  flex-grow: 1;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 12px;
}

.teacher-name {
  font-size: 22px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 1;
}

.apply-state {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  white-space: nowrap;
  z-index: 5;
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  color: #856404;
  border: 1px solid #ffeaa7;
}

.apply-state:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

/* 已读/删除/撤销按钮样式 */
.read-delete-button {
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
  color: white;
  z-index: 10;
  flex-shrink: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.read-delete-button:hover {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.state-pending {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
  color: #856404;
  border: 1px solid #ffeaa7;
}

.state-approved {
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  color: #155724;
  border: 1px solid #c3e6cb;
}

.state-rejected {
  background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.card-content {
  display: flex;
  flex-wrap: wrap;
  gap: 32px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255, 255, 255, 0.6);
  padding: 12px 20px;
  border-radius: 12px;
  border: 1px solid rgba(0, 0, 0, 0.03);
  transition: all 0.3s ease;
}

.info-item:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(102, 126, 234, 0.2);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.08);
}

.info-label {
  font-size: 14px;
  color: #718096;
  font-weight: 500;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 6px;
}

.info-label::before {
  content: '•';
  color: #667eea;
  font-weight: bold;
  font-size: 16px;
}

.info-value {
  font-size: 15px;
  color: #2d3748;
  font-weight: 600;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 添加一些微动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.apply-info-card {
  animation: fadeInUp 0.6s ease-out;
}

/* 卡片主体布局 */
.card-body {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  flex-wrap: wrap;
}

/* 操作按钮样式 */
.card-actions {
  display: flex;
  gap: 12px;
  margin-top: 0;
  padding-top: 0;
  border-top: none;
  justify-content: flex-end;
  flex-shrink: 0;
}

.action-button {
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.action-button:active {
  transform: translateY(0);
}

.approve-button {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  color: white;
}

.approve-button:hover {
  background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
}

.reject-button {
  background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
  color: white;
}

.reject-button:hover {
  background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
}



/* 响应式设计 */
@media (max-width: 768px) {
    .apply-info-card {
      padding: 20px 24px;
      margin-bottom: 20px;
    }
    
    /* 移动端状态徽章位置 */
    .status-badge {
      position: static;
      margin-bottom: 12px;
      align-self: flex-start;
    }
    
    .card-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 20px;
      position: relative;
    }
    
    .header-main {
      width: 100%;
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }
    
    .header-content {
      width: 100%;
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }
    
    .teacher-name {
      font-size: 20px;
      margin-top: 0;
    }
    
    /* 移动端按钮样式 */
    .read-delete-button {
      position: absolute;
      top: 16px;
      right: 16px;
      font-size: 12px;
      padding: 8px 16px;
      min-width: auto;
    }
  
  .card-body {
    flex-direction: column;
  }
  
  .card-content {
    flex-direction: column;
    gap: 12px;
    margin-bottom: 16px;
  }
  
  .card-actions {
    justify-content: stretch;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
  }
  
  .action-button {
    flex: 1;
    padding: 8px 16px;
  }
  
  .info-item {
    padding: 10px 16px;
  }
}

@media (max-width: 480px) {
    .apply-info-card {
      padding: 16px 20px;
    }
    
    .teacher-name {
      font-size: 18px;
    }
  
  .apply-state {
    padding: 4px 12px;
    font-size: 12px;
  }
  
  .info-item {
    padding: 8px 12px;
  }
  
  .info-label,
  .info-value {
    font-size: 13px;
  }
  
  .card-actions {
    gap: 8px;
  }
  
  .action-button,
  .read-delete-button {
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style>