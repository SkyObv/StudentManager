<script>
import TripsCard from '@/components/publicComp/TripsCard.vue'
import TripsCardAdd from '@/components/publicComp/TripsCardAdd.vue'
// 门禁卡管理组件
export default {
  name: 'CardIDManage',
  data() {
    return {
      tripscards: [],
      isEdit: false,                                                                     // 是否编辑状态
    }
  },
  created() {
    this.getTripsCards()                                                                 // 初始化时获取所有门禁卡信息
  },
  methods: {
    getTripsCards() {                                                                    // http请求获取所有门禁卡信息
        this.$axios({
          url: `${this.$settings.Host}/teacher/trips/get/all`,
          method: 'get',
          headers: {Authorization: `Hander ${this.$settings.getToken()}`}
      }).then(res => {
        this.tripscards = res.data
      }).catch(err => {
        console.log(err)
        this.$message.error('获取门禁卡信息失败')
      })
    },
    editCard() {                                                                         // 编辑门禁卡
    this.isEdit = !this.isEdit
    },
  },
  components: {
    TripsCard,
    TripsCardAdd,
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

      <!-- 功能区域 -->
      <div class="function-area">
        <button class="action-button edit-button" @click="editCard">
          <span class="button-icon">✏️</span>
          添加门禁卡
        </button>
      </div>

      <!-- 提示区域 -->
      <div class="card-stats">
        <div class="stats-item">
          <span class="stats-label">门禁卡总数：</span>
          <span class="stats-value">{{ tripscards.length }}</span>
        </div>
      </div>
      
      <!-- 门禁卡卡片区域 -->
      <div class="card-container" v-if="isEdit===false">
        <TripsCard 
        v-for="card in tripscards" 
        :key="card.id" 
        :keyCard="card"
        @updateCard="getTripsCards"></TripsCard>
      </div>

      <!-- 编辑门禁卡卡片区域 -->
      <div v-if="isEdit===true" class="edit-card-container">
        <div class="edit-card-wrapper">
          <TripsCardAdd></TripsCardAdd>
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

/* 功能区域 */
.function-area {
  display: flex;
  justify-content: flex-start;
  gap: 12px;
  margin-bottom: 24px;
  animation: fadeInUp 0.6s ease-out 0.2s both;
}

.action-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 24px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  min-width: 120px;
  justify-content: center;
  line-height: 20px;
  min-height: 40px;
}

.action-button:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.button-icon {
  font-size: 14px;
}

/* 编辑门禁卡容器 */
.edit-card-container {
  margin-top: 24px;
  animation: fadeInUp 0.6s ease-out 0.4s both;
}

.edit-card-wrapper {
  background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.5);
  padding: 24px;
  margin-bottom: 32px;
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