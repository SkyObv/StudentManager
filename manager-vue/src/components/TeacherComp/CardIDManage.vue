<script>
import TripsCard from '@/components/publicComp/TripsCard.vue'
// 门禁卡管理组件
export default {
  name: 'CardIDManage',
  data() {
    return {
      tripscards: [],
    }
  },
  created() {
    this.getTripsCards()                                                                 // 初始化时获取所有门禁卡信息
  },
  methods: {
    getTripsCards() {                                                                    // http请求获取所有门禁卡信息
      console.log('获取所有门禁卡信息')
    },
  },
  components: {
    TripsCard,
  }
}
</script>

<template>
  <div class="card-id-container">
    <div class="content-container">

      <!-- 标题区域 -->
      <div class="page-header">
        <h1 class="page-title">门禁卡管理</h1>
        <p class="page-subtitle">管理学生的门禁卡信息</p>
      </div>

      <!-- 提示区域 -->
      <div class="card-stats">
        <div class="stats-item">
          <span class="stats-label">门禁卡总数：</span>
          <span class="stats-value">{{ tripscards.length }}</span>
        </div>
      </div>
      
      <!-- 门禁卡卡片区域 -->
      <div class="card-container">
        <TripsCard 
        v-for="card in tripscards" 
        :key="card.id" 
        :keyCard="card"></TripsCard>
      </div>
      
    </div>
  </div>
</template>

<style scoped>
/* 页面容器 */
.card-id-container {
  padding: 2rem;
  font-family: Arial, sans-serif;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
  animation: pageFadeIn 0.6s ease-out;
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

/* 门禁卡卡片区域 */
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: flex-start;
  width: 100%;
}

/* 提示区域 */
.card-stats {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 16px 24px;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.5);
  animation: fadeInUp 0.6s ease-out 0.3s both;
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
</style>