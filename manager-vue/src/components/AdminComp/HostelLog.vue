<script>
// 宿舍申请审批
import ApplyInfoCard from "@/components/publicComp/ApplyInfoCard.vue"; // 申请记录卡片

export default {
  name : 'HostelLog',
  components: {
    ApplyInfoCard
  },
  data() {
    return {
      applyInfos: [
        {
          id: 1,
          teacher_name : '测试老师1',
          apply_state : '待审核',
          apply_time : '2025-01-01 10:00:00',
          hostel_name: '1号楼101宿舍'
        },
        {
          id: 2,
          teacher_name : '测试老师2',
          apply_state : '已通过',
          apply_time : '2025-01-02 14:30:00',
          hostel_name: '2号楼202宿舍'
        },
        {
          id: 3,
          teacher_name : '测试老师3',
          apply_state : '已拒绝',
          apply_time : '2025-01-03 09:15:00',
          hostel_name: '3号楼303宿舍'
        }
      ],
      loading: false,
      selectedState: '',
      states: [
        { value: '', label: '全部状态' },
        { value: '待审核', label: '待审核' },
        { value: '已通过', label: '已通过' },
        { value: '已拒绝', label: '已拒绝' }
      ]
    }
  },
  // 函数方法
  methods: {
    // 处理状态筛选变化
    handleStateChange() {
      // 这里可以添加筛选逻辑
      console.log('筛选状态:', this.selectedState);
    },
    // 处理同意按钮点击
    handleApprove(item) {
      console.log('同意申请:', item);
      // 这里可以添加同意申请的逻辑
    },
    // 处理拒绝按钮点击
    handleReject(item) {
      console.log('拒绝申请:', item);
      // 这里可以添加拒绝申请的逻辑
    }
  },
  // 页面创建启动方法
  created() {
  }
}
</script>

<template>
  <div class="apply-container">
    <!-- 标题区域 -->
    <div class="page-header">
      <h1 class="page-title">宿舍申请审批</h1>
      <p class="page-subtitle">管理和审批教师的宿舍申请</p>
    </div>
    
    <!-- 筛选区域 -->
    <div class="search-filter">
      <select v-model="selectedState" @change="handleStateChange" class="filter-select">
        <option v-for="state in states" :key="state.value" :value="state.value">{{ state.label }}</option>
      </select>
    </div>
    
    <!-- 申请列表区域 -->
    <div class="apply-list">
      <ApplyInfoCard 
        v-for="item in applyInfos" 
        :key="item.id" 
        :applyInfo="item"
        :showActionButtons="true"
        @approve="handleApprove"
        @reject="handleReject"
      ></ApplyInfoCard>
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="applyInfos.length === 0" class="empty-data">暂无申请数据</div>
    </div>
  </div>
</template>

<style scoped>
/* 容器样式 */
.apply-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px;
  min-height: 100vh;
  background-color: #f8fafc;
  width: 100%;
  box-sizing: border-box;
}

/* 标题区域 */
.page-header {
  text-align: center;
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
  margin-bottom: 0.5rem;
  animation: fadeInUp 0.8s ease-out;
}

.page-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  font-weight: 400;
  animation: fadeInUp 0.8s ease-out 0.2s both;
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

.filter-select {
  padding: 12px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background-color: white;
  color: #303133;
  min-width: 150px;
}

.filter-select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

/* 申请列表区域 */
.apply-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
  padding: 24px;
  width: 100%;
  box-sizing: border-box;
}

/* 确保卡片宽度与容器一致 */
.apply-list :deep(.apply-info-card) {
  width: 100%;
  box-sizing: border-box;
}

/* 无数据状态 */
.empty-data {
  text-align: center;
  padding: 60px 20px;
  font-size: 16px;
  color: #909399;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
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

/* 响应式设计 */
@media (max-width: 768px) {
  .apply-container {
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
  
  .filter-select {
    width: 100%;
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .apply-container {
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
</style>