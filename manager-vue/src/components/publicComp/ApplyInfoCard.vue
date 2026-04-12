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
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 20px 24px;
  margin-bottom: 16px;
  border: 1px solid #e2e8f0;
  position: relative;
  will-change: transform;
}

.apply-info-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #667eea;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
  gap: 8px;
}

.header-main {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-grow: 1;
  overflow: hidden;
}

.header-content {
  flex-grow: 1;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 10px;
}

.teacher-name {
  font-size: 18px;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 1;
}

.apply-state {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
  z-index: 5;
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

/* 已读/删除/撤销按钮样式 */
.read-delete-button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  background: #4a5568;
  color: white;
  z-index: 10;
  flex-shrink: 0;
}

.read-delete-button:hover {
  background: #2d3748;
}

.state-pending {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeaa7;
}

.state-approved {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.state-rejected {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.card-content {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #f8fafc;
  padding: 10px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.info-label {
  font-size: 13px;
  color: #718096;
  font-weight: 500;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 4px;
}

.info-label::before {
  content: '•';
  color: #667eea;
  font-weight: bold;
  font-size: 14px;
}

.info-value {
  font-size: 14px;
  color: #2d3748;
  font-weight: 500;
}

/* 卡片主体布局 */
.card-body {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  flex-wrap: wrap;
}

/* 操作按钮样式 */
.card-actions {
  display: flex;
  gap: 8px;
  margin-top: 0;
  padding-top: 0;
  border-top: none;
  justify-content: flex-end;
  flex-shrink: 0;
}

.action-button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
}

.approve-button {
  background: #48bb78;
  color: white;
}

.approve-button:hover {
  background: #38a169;
}

.reject-button {
  background: #f56565;
  color: white;
}

.reject-button:hover {
  background: #e53e3e;
}



/* 响应式设计 */
@media (max-width: 768px) {
    .apply-info-card {
      padding: 16px 20px;
      margin-bottom: 16px;
    }
    
    .card-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
      margin-bottom: 16px;
      position: relative;
    }
    
    .header-main {
      width: 100%;
      flex-direction: column;
      align-items: flex-start;
      gap: 6px;
    }
    
    .header-content {
      width: 100%;
      flex-direction: column;
      align-items: flex-start;
      gap: 6px;
    }
    
    .teacher-name {
      font-size: 16px;
      margin-top: 0;
    }
    
    /* 移动端按钮样式 */
    .read-delete-button {
      position: absolute;
      top: 12px;
      right: 12px;
      font-size: 10px;
      padding: 6px 12px;
    }
  
  .card-body {
    flex-direction: column;
  }
  
  .card-content {
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
  }
  
  .card-actions {
    justify-content: stretch;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #f1f5f9;
  }
  
  .action-button {
    flex: 1;
    padding: 6px 12px;
  }
  
  .info-item {
    padding: 8px 12px;
  }
}

@media (max-width: 480px) {
    .apply-info-card {
      padding: 12px 16px;
    }
    
    .teacher-name {
      font-size: 14px;
    }
  
  .apply-state {
    padding: 3px 10px;
    font-size: 10px;
  }
  
  .info-item {
    padding: 6px 10px;
  }
  
  .info-label,
  .info-value {
    font-size: 12px;
  }
  
  .card-actions {
    gap: 6px;
  }
  
  .action-button,
  .read-delete-button {
    padding: 4px 8px;
    font-size: 10px;
  }
}
</style>