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
      batchCreating: false, // 批量创建加载状态
      // 批量绑定老师相关
      editMode: false, // 编辑模式状态
      selectedCards: [], // 选中的门禁卡
      teacherUsername: '', // 老师账号
      searchTeacherLoading: false, // 搜索老师加载状态
      foundTeacher: null, // 找到的老师信息
      searchError: '' // 搜索错误信息
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
    },
    /**
     * 切换编辑模式
     */
    toggleEditMode() {
      this.editMode = !this.editMode;
      // 重置选中的门禁卡
      this.selectedCards = [];
      // 重置老师搜索相关数据
      this.teacherUsername = '';
      this.foundTeacher = null;
      this.searchError = '';
    },
    /**
     * 搜索老师
     */
    searchTeacher() {
      if (!this.teacherUsername.trim()) {
        this.$message.error('请输入老师账号');
        return;
      }
      
      this.searchTeacherLoading = true;
      this.searchError = '';
      
      this.$axios({
        url: `${this.$settings.Host}/users/teachers/`,
        method: 'get',
        params: {
          username: this.teacherUsername.trim()
        },
        headers: {
          'Authorization': `Hander ${this.$settings.getToken()}`
        }
      }).then(res => {
        console.log('搜索老师结果:', res.data);
        if (res.data && res.data.length > 0) {
          this.foundTeacher = res.data[0];
          this.searchError = '';
          this.$message.success(`找到老师: ${this.foundTeacher.name}`);
        } else {
          this.foundTeacher = null;
          this.searchError = '未找到该老师账号';
          this.$message.error('未找到该老师账号');
        }
      }).catch(err => {
        console.error('搜索老师失败:', err);
        this.foundTeacher = null;
        this.searchError = '搜索老师失败，请重试';
        this.$message.error('搜索老师失败，请重试');
      }).finally(() => {
        this.searchTeacherLoading = false;
      });
    },
    /**
     * 选择/取消选择门禁卡
     * @param {number} cardId - 门禁卡ID
     */
    toggleCardSelection(cardId) {
      const index = this.selectedCards.indexOf(cardId);
      if (index > -1) {
        // 取消选择
        this.selectedCards.splice(index, 1);
      } else {
        // 选择
        this.selectedCards.push(cardId);
      }
    },
    /**
     * 批量绑定老师
     */
    batchBindTeacher() {
      if (this.selectedCards.length === 0) {
        this.$message.error('请至少选择一张门禁卡');
        return;
      }
      
      if (!this.foundTeacher) {
        this.$message.error('请先搜索并选择老师');
        return;
      }
      
      this.batchCreating = true;
      
      // 构建请求数据
      const requestData = {
        card_ids: this.selectedCards,
        teacher_id: this.foundTeacher.id
      };
      
      // 发送批量绑定老师请求
      this.$axios({
        url: `${this.$settings.Host}/users/card/update/manager`,
        method: 'post',
        data: requestData,
        headers: {
          'Authorization': `Hander ${this.$settings.getToken()}`
        }
      }).then(res => {
        console.log('批量绑定老师成功:', res.data);
        this.$message.success(res.data.message || '批量绑定老师成功');
        // 重置状态
        this.editMode = false;
        this.selectedCards = [];
        this.teacherUsername = '';
        this.foundTeacher = null;
        this.searchError = '';
        // 重新获取门禁卡列表
        this.getCardList();
      }).catch(err => {
        console.error('批量绑定老师失败:', err);
        this.$message.error('批量绑定老师失败，请重试');
      }).finally(() => {
        // 隐藏加载状态
        this.batchCreating = false;
      });
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
        <!-- 操作按钮 -->
        <div class="header-actions">
          <button 
            class="edit-mode-button" 
            :class="{ 'active': editMode }"
            @click="toggleEditMode"
          >
            <span class="button-icon">{{ editMode ? '✓' : '✏️' }}</span>
            {{ editMode ? '退出编辑' : '编辑模式' }}
          </button>
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

      <!-- 老师搜索区域（编辑模式下显示） -->
      <div v-if="editMode" class="teacher-search-container">
        <div class="search-header">
          <h3 class="search-title">批量绑定老师</h3>
          <p class="search-subtitle">请搜索并选择老师，然后选择要绑定的门禁卡</p>
        </div>
        <div class="search-form">
          <div class="search-item">
            <label for="teacher-username">老师账号：</label>
            <input 
              type="text" 
              id="teacher-username"
              v-model="teacherUsername"
              placeholder="请输入老师账号"
              class="search-input"
            >
            <button 
              class="search-button" 
              :disabled="searchTeacherLoading"
              @click="searchTeacher"
            >
              <span v-if="searchTeacherLoading" class="loading-spinner small"></span>
              {{ searchTeacherLoading ? '搜索中...' : '搜索' }}
            </button>
          </div>
          <div v-if="foundTeacher" class="teacher-info">
            <p class="teacher-name">找到老师：{{ foundTeacher.name }} ({{ foundTeacher.username }})</p>
          </div>
          <div v-if="searchError" class="search-error">
            {{ searchError }}
          </div>
          <div class="selected-info">
            <p>已选择 {{ selectedCards.length }} 张门禁卡</p>
            <button 
              v-if="selectedCards.length > 0 && foundTeacher"
              class="bind-button"
              :disabled="batchCreating"
              @click="batchBindTeacher"
            >
              <span v-if="batchCreating" class="loading-spinner small"></span>
              {{ batchCreating ? '绑定中...' : '批量绑定老师' }}
            </button>
          </div>
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
        <div v-for="card in tripscards" :key="card.id" class="card-wrapper">
          <!-- 选择复选框（编辑模式下显示） -->
          <div v-if="editMode" class="card-checkbox">
            <input 
              type="checkbox" 
              :id="`card-${card.id}`"
              :checked="selectedCards.includes(card.id)"
              @change="toggleCardSelection(card.id)"
            >
            <label :for="`card-${card.id}`"></label>
          </div>
          <TripsCard 
            :keyCard="card"
            :type="'admin'"
            @updateCard="handleUpdateCard"
            @bindStudent="handleBindStudent"
          ></TripsCard>
        </div>
        
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
  display: flex;
  gap: 12px;
  justify-content: center;
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

/* 编辑模式按钮 */
.edit-mode-button {
  padding: 10px 20px;
  background-color: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.edit-mode-button:hover {
  background-color: #e2e8f0;
}

.edit-mode-button.active {
  background-color: #10b981;
  color: white;
  border-color: #10b981;
}

.edit-mode-button.active:hover {
  background-color: #059669;
}

.edit-mode-button .button-icon {
  font-size: 16px;
}

/* 老师搜索区域 */
.teacher-search-container {
  margin-bottom: 24px;
  padding: 20px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.search-header {
  margin-bottom: 16px;
}

.search-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 4px 0;
}

.search-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.search-item {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.search-item label {
  font-weight: 500;
  white-space: nowrap;
  color: #4a5568;
  font-size: 14px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  width: 200px;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-button {
  padding: 8px 16px;
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

.search-button:hover {
  background-color: #2563eb;
}

.search-button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.teacher-info {
  padding: 12px;
  background-color: #d1fae5;
  border-radius: 6px;
  border: 1px solid #a7f3d0;
}

.teacher-name {
  margin: 0;
  color: #065f46;
  font-size: 14px;
}

.search-error {
  padding: 12px;
  background-color: #fee2e2;
  border-radius: 6px;
  border: 1px solid #fecaca;
  color: #dc2626;
  font-size: 14px;
}

.selected-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background-color: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.selected-info p {
  margin: 0;
  color: #475569;
  font-size: 14px;
}

.bind-button {
  padding: 8px 16px;
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

.bind-button:hover {
  background-color: #059669;
}

.bind-button:disabled {
  background-color: #6ee7b7;
  cursor: not-allowed;
}

/* 小加载动画 */
.loading-spinner.small {
  width: 12px;
  height: 12px;
  border-width: 1px;
}

/* 门禁卡包装器 */
.card-wrapper {
  position: relative;
  width: calc(33.333% - 16px);
  max-width: 384px;
  flex: 0 0 calc(33.333% - 16px);
}

/* 卡片复选框 */
.card-checkbox {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 10;
}

.card-checkbox input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.card-checkbox label {
  display: block;
  position: relative;
  padding-left: 28px;
  margin-bottom: 12px;
  cursor: pointer;
  font-size: 16px;
  user-select: none;
}

.card-checkbox label::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  height: 20px;
  width: 20px;
  background-color: white;
  border: 2px solid #3b82f6;
  border-radius: 4px;
}

.card-checkbox input[type="checkbox"]:checked + label::before {
  background-color: #3b82f6;
}

.card-checkbox label::after {
  content: "";
  position: absolute;
  display: none;
  left: 7px;
  top: 3px;
  width: 6px;
  height: 12px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.card-checkbox input[type="checkbox"]:checked + label::after {
  display: block;
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
  gap: 12px;
  justify-content: flex-start;
  width: 100%;
  margin-bottom: 24px;
}

/* 门禁卡包装器 */
.card-wrapper {
  position: relative;
  width: calc(33.333% - 8px);
  max-width: 384px;
  flex: 0 0 calc(33.333% - 8px);
  box-sizing: border-box;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .card-wrapper {
    width: calc(50% - 6px);
    flex: 0 0 calc(50% - 6px);
  }
}

@media (max-width: 768px) {
  .card-wrapper {
    width: 100%;
    flex: 0 0 100%;
  }
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

