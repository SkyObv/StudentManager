<script>
import ApplyInfoCard from '@/components/publicComp/ApplyInfoCard.vue'
export default {
  name: 'ApplyHostel',
  data() {
    return {
      applyInfos: [
        {
          id: 1,
          teacher_name: '大大怪',
          hostel_name: '2-101',
          apply_time: '2025-12-12T14:44:11.096746+08:00',
          apply_state: '待审核'
        },
        {
          id: 2,
          teacher_name: '大大怪',
          hostel_name: '2-101',
          apply_time: '2025-12-12T14:44:11.096746+08:00',
          apply_state: '已审核'
        },
      ],
    }
  },
  components: {
    ApplyInfoCard
  },
}
</script>

<template>
  <div class="apply-container">
    <!-- 标题区域 -->
    <div class="page-header">
      <h1 class="page-title">宿舍申请管理</h1>
      <p class="page-subtitle">处理学生的宿舍申请</p>
    </div>
    
    <!-- 筛选区域 -->
    <div class="search-filter">
      <select class="filter-select">
        <option value="">全部状态</option>
        <option value="待审核">待审核</option>
        <option value="已通过">已通过</option>
        <option value="已拒绝">已拒绝</option>
      </select>
    </div>
    
    <!-- 申请列表区域 -->
    <div class="apply-list">
      <ApplyInfoCard 
        v-for="item in applyInfos" 
        :key="item.id" 
        :applyInfo="item"
      ></ApplyInfoCard>
      <div v-if="applyInfos.length === 0" class="empty-data">暂无申请数据</div>
    </div>
  </div>
</template>

<style scoped>
/* 容器样式 */
.apply-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px;
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* 标题区域 */
.page-header {
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
  margin: 0 0 8px 0;
  letter-spacing: 0.5px;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.page-subtitle {
  font-size: 16px;
  color: #909399;
  margin: 0;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
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
</style>