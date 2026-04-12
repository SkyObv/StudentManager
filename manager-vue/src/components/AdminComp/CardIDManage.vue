<script>
import TripsCard from '@/components/publicComp/TripsCard.vue';

export default {
  name: 'AdminCardIDManage',
  components: {
    TripsCard
  },
  data() {
    return {
      tripscards: [], // 门禁卡列表
      totalCount: 0, // 总数量
      loading: false, // 加载状态
      error: '', // 错误信息
      currentPage: 1, // 当前页码
      pageSize: 20, // 每页显示数量
      nextPage: null, // 下一页URL
      previousPage: null, // 上一页URL
      // 过滤参数
      filters: {
        has_manager: null, // 是否有管理员
        number: '' // 卡号搜索
      },
      // 批量创建相关
      batchCreateDialog: false, // 批量创建对话框显示状态
      batchCardNumbers: [{ number: '' }], // 批量创建的卡号列表
      maxCardCount: 50, // 最大批量创建数量
      batchCreating: false // 批量创建加载状态
    }
  },
  mounted() {
    // 组件挂载后获取门禁卡数据
    this.getCardList();
  },
  methods: {
    /**
     * 获取门禁卡列表数据
     * @param {string} url - 请求URL，默认为第一页
     */
    getCardList(url) {
      this.loading = true;
      this.error = '';
      
      // 构建请求URL和参数
      let requestUrl = url || `${this.$settings.Host}/users/card/all/`;
      const params = {};
      
      // 添加过滤参数
      if (this.filters.has_manager !== null) {
        params.has_manager = this.filters.has_manager;
      }
      if (this.filters.number) {
        params.number = this.filters.number;
      }
      
      // 发送请求
      this.$axios({
        url: requestUrl,
        method: 'get',
        params: params,
        headers: {
          'Authorization': `Hander ${this.$settings.getToken()}`
        }
      }).then(res => {
        console.log('获取门禁卡列表成功:', res.data);
        // 更新数据
        this.tripscards = res.data.results;
        this.totalCount = res.data.count;
        this.nextPage = res.data.next;
        this.previousPage = res.data.previous;
      }).catch(err => {
        console.error('获取门禁卡列表失败:', err);
        this.error = '获取门禁卡列表失败，请重试';
        this.tripscards = [];
        this.totalCount = 0;
      }).finally(() => {
        this.loading = false;
      });
    },
    /**
     * 处理过滤条件变化
     */
    handleFilterChange() {
      // 重置页码
      this.currentPage = 1;
      // 重新获取数据
      this.getCardList();
    },
    /**
     * 重置过滤条件
     */
    resetFilters() {
      this.filters = {
        has_manager: null,
        number: ''
      };
      // 重新获取数据
      this.handleFilterChange();
    },
    /**
     * 打开批量创建对话框
     */
    openBatchCreateDialog() {
      // 重置批量创建表单
      this.batchCardNumbers = [{ number: '' }];
      // 显示对话框
      this.batchCreateDialog = true;
    },
    /**
     * 关闭批量创建对话框
     */
    closeBatchCreateDialog() {
      // 隐藏对话框
      this.batchCreateDialog = false;
    },
    /**
     * 添加卡号输入行
     */
    addCardNumber() {
      if (this.batchCardNumbers.length < this.maxCardCount) {
        this.batchCardNumbers.push({ number: '' });
      }
    },
    /**
     * 删除卡号输入行
     * @param {number} index - 要删除的行索引
     */
    removeCardNumber(index) {
      if (this.batchCardNumbers.length > 1) {
        this.batchCardNumbers.splice(index, 1);
      }
    },
    /**
     * 提交批量创建请求
     */
    submitBatchCreate() {
      // 验证所有卡号是否为空
      const validCards = this.batchCardNumbers.filter(card => card.number.trim() !== '');
      if (validCards.length === 0) {
        this.$message.error('请至少填写一个卡号');
        return;
      }
      
      // 显示加载状态
      this.batchCreating = true;
      
      // 发送请求
      this.$axios({
        url: `${this.$settings.Host}/users/card/creates/`,
        method: 'post',
        data: validCards,
        headers: {
          'Authorization': `Hander ${this.$settings.getToken()}`
        }
      }).then(res => {
        console.log('批量创建门禁卡成功:', res.data);
        this.$message.success('批量创建门禁卡成功');
        // 关闭对话框
        this.closeBatchCreateDialog();
        // 重新获取门禁卡列表
        this.getCardList();
      }).catch(err => {
        console.error('批量创建门禁卡失败:', err);
        // 处理错误响应
        if (err.response && err.response.data) {
          const errorData = err.response.data;
          // 检查是否是卡号已存在的错误格式
          if (Array.isArray(errorData) && errorData.length > 0) {
            const errorMessages = [];
            errorData.forEach((error, index) => {
              if (error.number && Array.isArray(error.number)) {
                errorMessages.push(`第 ${index + 1} 个卡号: ${error.number.join(', ')}`);
              }
            });
            if (errorMessages.length > 0) {
              this.$message.error(`批量创建失败:\n${errorMessages.join('\n')}`);
              return;
            }
          }
        }
        // 其他错误
        this.$message.error('批量创建门禁卡失败，请重试');
      }).finally(() => {
        // 隐藏加载状态
        this.batchCreating = false;
      });
    },
    /**
     * 处理分页点击
     * @param {string} type - 分页类型：prev, next
     */
    handlePagination(type) {
      if (type === 'prev' && this.previousPage) {
        this.currentPage--;
        this.getCardList(this.previousPage);
      } else if (type === 'next' && this.nextPage) {
        this.currentPage++;
        this.getCardList(this.nextPage);
      }
    },
    /**
     * 处理门禁卡更新
     */
    handleUpdateCard() {
      // 重新获取门禁卡列表
      this.getCardList();
    },
    /**
     * 处理绑定学生
     * @param {number} cardId - 门禁卡ID
     */
    handleBindStudent(cardId) {
      console.log('绑定学生:', cardId);
      // 这里可以实现绑定学生的逻辑
    }
  }
}
</script>

<template>
  <div class="card-id-container">
    <div class="content-container">
      <!-- 标题区域 -->
      <div class="page-header">
        <h1 class="page-title">门禁卡管理</h1>
        <p class="page-subtitle">管理所有的门禁卡信息</p>
        <!-- 批量创建按钮 -->
        <div class="header-actions">
          <button class="batch-create-button" @click="openBatchCreateDialog">
            <span class="button-icon">➕</span>
            批量创建门禁卡
          </button>
        </div>
      </div>

      <!-- 提示区域 -->
      <div class="card-stats">
        <div class="stats-item">
          <span class="stats-label">门禁卡总数：</span>
          <span class="stats-value">{{ totalCount }}</span>
        </div>
      </div>

      <!-- 过滤区域 -->
      <div class="filter-container">
        <div class="filter-item">
          <label for="number-filter">卡号搜索：</label>
          <input 
            type="text" 
            id="number-filter"
            v-model="filters.number"
            placeholder="请输入卡号"
            class="filter-input"
            @input="handleFilterChange"
          >
        </div>
        <div class="filter-item">
          <label for="has-manager-filter">是否有管理员：</label>
          <select 
            id="has-manager-filter"
            v-model="filters.has_manager"
            class="filter-select"
            @change="handleFilterChange"
          >
            <option value="">全部</option>
            <option value="true">有</option>
            <option value="false">无</option>
          </select>
        </div>
        <div class="filter-item">
          <button class="reset-button" @click="resetFilters">
            重置过滤
          </button>
        </div>
      </div>

      <!-- 错误提示 -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p class="loading-text">加载中...</p>
      </div>

      <!-- 门禁卡列表 -->
      <div v-else class="card-container">
        <TripsCard 
          v-for="card in tripscards" 
          :key="card.id" 
          :keyCard="card"
          :type="'admin'"
          @updateCard="handleUpdateCard"
          @bindStudent="handleBindStudent"
        ></TripsCard>
        
        <!-- 无数据状态 -->
        <div v-if="tripscards.length === 0" class="empty-container">
          <p class="empty-text">暂无门禁卡数据</p>
        </div>
      </div>

      <!-- 分页区域 -->
      <div v-if="totalCount > 0" class="pagination-container">
        <button 
          class="pagination-button" 
          :disabled="!previousPage"
          @click="handlePagination('prev')"
        >
          上一页
        </button>
        <span class="pagination-info">
          第 {{ currentPage }} 页，共 {{ Math.ceil(totalCount / pageSize) }} 页
        </span>
        <button 
          class="pagination-button" 
          :disabled="!nextPage"
          @click="handlePagination('next')"
        >
          下一页
        </button>
      </div>

      <!-- 批量创建对话框 -->
      <div v-if="batchCreateDialog" class="dialog-overlay">
        <div class="dialog-container">
          <div class="dialog-header">
            <h2 class="dialog-title">批量创建门禁卡</h2>
            <button class="dialog-close" @click="closeBatchCreateDialog">×</button>
          </div>
          <div class="dialog-body">
            <div class="batch-form">
              <div class="form-description">
                <p>请输入要创建的门禁卡卡号，最多可同时创建 {{ maxCardCount }} 个门禁卡。</p>
              </div>
              <div class="card-numbers-list">
                <div 
                  v-for="(card, index) in batchCardNumbers" 
                  :key="index"
                  class="card-number-item"
                >
                  <div class="card-number-index">
                    {{ index + 1 }}
                  </div>
                  <div class="card-number-input">
                    <input 
                      type="text" 
                      v-model="card.number"
                      placeholder="请输入卡号"
                      class="number-input"
                    >
                  </div>
                  <div class="card-number-actions">
                    <button 
                      v-if="batchCardNumbers.length > 1"
                      class="remove-button"
                      @click="removeCardNumber(index)"
                    >
                      ×
                    </button>
                  </div>
                </div>
              </div>
              <div class="add-card-button">
                <button 
                  v-if="batchCardNumbers.length < maxCardCount"
                  class="add-button"
                  @click="addCardNumber"
                >
                  <span class="button-icon">➕</span>
                  添加卡号
                </button>
              </div>
            </div>
          </div>
          <div class="dialog-footer">
            <button class="cancel-button" @click="closeBatchCreateDialog">
              取消
            </button>
            <button 
              class="submit-button" 
              :disabled="batchCreating"
              @click="submitBatchCreate"
            >
              <span v-if="batchCreating" class="loading-spinner"></span>
              {{ batchCreating ? '创建中...' : '提交' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 页面容器 */
.card-id-container {
  padding: 2rem;
  font-family: Arial, sans-serif;
  background: #f8fafc;
  min-height: 100vh;
}

/* 内容容器 */
.content-container {
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  padding: 0 20px;
}

/* 标题区域 */
.page-header {
  text-align: center;
  margin-bottom: 2rem;
  color: #1e293b;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #3b82f6;
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  font-weight: 400;
  margin-bottom: 1rem;
}

/* 标题区域按钮 */
.header-actions {
  margin-top: 1rem;
}

.batch-create-button {
  padding: 10px 20px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.batch-create-button:hover {
  background-color: #2563eb;
}

.batch-create-button .button-icon {
  font-size: 16px;
}

/* 对话框样式 */
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

.dialog-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.dialog-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.dialog-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #64748b;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.dialog-close:hover {
  background-color: #f1f5f9;
}

.dialog-body {
  padding: 24px;
}

.batch-form {
  width: 100%;
}

.form-description {
  margin-bottom: 20px;
}

.form-description p {
  color: #64748b;
  font-size: 14px;
  margin: 0;
}

.card-numbers-list {
  margin-bottom: 20px;
}

.card-number-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.card-number-index {
  width: 32px;
  height: 32px;
  background-color: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
  flex-shrink: 0;
}

.card-number-input {
  flex: 1;
}

.number-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.2s ease;
}

.number-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.card-number-actions {
  flex-shrink: 0;
}

.remove-button {
  width: 32px;
  height: 32px;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease;
}

.remove-button:hover {
  background-color: #f87171;
}

.add-card-button {
  margin-bottom: 20px;
}

.add-button {
  padding: 10px 16px;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.add-button:hover {
  background-color: #059669;
}

.add-button .button-icon {
  font-size: 16px;
}

.dialog-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e2e8f0;
}

.cancel-button {
  padding: 10px 20px;
  background-color: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-button:hover {
  background-color: #e2e8f0;
}

.submit-button {
  padding: 10px 20px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.submit-button:hover {
  background-color: #2563eb;
}

.submit-button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 门禁卡卡片区域 */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: flex-start;
  width: 100%;
  margin-bottom: 24px;
}

/* 提示区域 */
.card-stats {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 16px 24px;
  margin-bottom: 24px;
  border: 1px solid #e2e8f0;
}

.stats-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stats-label {
  font-size: 14px;
  color: #718096;
  font-weight: 500;
}

.stats-value {
  font-size: 18px;
  color: #3b82f6;
  font-weight: 700;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 过滤区域 */
.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px 24px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-item label {
  font-weight: 500;
  white-space: nowrap;
  color: #4a5568;
  font-size: 14px;
}

.filter-input {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  width: 200px;
  transition: all 0.2s ease;
}

.filter-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  width: 150px;
  transition: all 0.2s ease;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.reset-button {
  padding: 8px 16px;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.reset-button:hover {
  background-color: #f87171;
}

/* 错误提示 */
.error-message {
  background: #fef2f2;
  border: 1px solid #fee2e2;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 24px;
  color: #dc2626;
  font-size: 14px;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(59, 130, 246, 0.3);
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 20px;
}

.loading-text {
  font-size: 16px;
  color: #64748b;
  font-weight: 500;
}

/* 无数据状态 */
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  width: 100%;
}

.empty-text {
  font-size: 16px;
  color: #94a3b8;
  font-weight: 500;
}

/* 分页区域 */
.pagination-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
  padding: 16px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.pagination-button {
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: #ffffff;
  color: #3b82f6;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-button:hover:not(:disabled) {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.pagination-button:disabled {
  color: #94a3b8;
  cursor: not-allowed;
  background: #f8fafc;
}

.pagination-info {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pageFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .card-id-container {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .card-container {
    justify-content: center;
  }
  
  .pagination-container {
    flex-direction: column;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .card-id-container {
    padding: 0.75rem;
  }
  
  .page-title {
    font-size: 1.75rem;
  }
  
  .page-header {
    margin-bottom: 1.5rem;
  }
  
  .card-stats {
    padding: 12px 16px;
  }
}
</style>

