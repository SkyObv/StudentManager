<script>
import ApplyHostelCard from "@/components/publicComp/ApplyHostelCard.vue";
export default {
  components: {
    ApplyHostelCard                               // 宿舍信息卡片
  },
  data() {
    return {
      hostelList: [
          {
            "id": 2,
            "hostel_number": "1-102",
            "manager_name": null,
            "gender": "female",
            "floor_name": "1"
        },
          {
            "id": 2,
            "hostel_number": "1-102",
            "manager_name": null,
            "gender": "female",
            "floor_name": "1"
        },
          {
            "id": 2,
            "hostel_number": "1-102",
            "manager_name": null,
            "gender": "female",
            "floor_name": "1"
        },
          {
            "id": 2,
            "hostel_number": "1-102",
            "manager_name": null,
            "gender": "female",
            "floor_name": "1"
        },
      ],
      searchKeyword : null
    }
  }
}
</script>

<template>
  <div class="apply-hostel-container">
    <div class="apply-hostel-header">
      <h2 class="page-title">宿舍申请</h2>
      <!-- 搜索输入框 -->
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchKeyword" 
          placeholder="输入楼号搜索..." 
          class="search-input"
        >
      </div>
    </div>
    <div class="hostel-cards-wrapper">
      <ApplyHostelCard v-for="item in hostelList" :key="item.id" :hostelInfo="item"></ApplyHostelCard>
    </div>
  </div>
</template>

<style scoped>
/* 页面容器 */
.apply-hostel-container {
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
  color: #333;
  animation: pageFadeIn 0.6s ease-out;
}

/* 页面标题 */
.apply-hostel-header {
  text-align: center;
  margin-bottom: 3rem;
  color: #1e293b;
}

/* 页面标题 */
.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1.5rem;
  animation: fadeInUp 0.8s ease-out;
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 搜索容器 */
.search-container {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

/* 搜索输入框 */
.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  color: #374151;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  transform: translateY(-1px);
}

.search-input::placeholder {
  color: #9ca3af;
  font-weight: 400;
}

/* 卡片容器 */
.hostel-cards-wrapper {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* 动画效果 */
@keyframes pageFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

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

/* 响应式设计 */
@media (max-width: 768px) {
  .apply-hostel-container {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .hostel-cards-wrapper {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 480px) {
  .apply-hostel-container {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 1.75rem;
  }
}
</style>