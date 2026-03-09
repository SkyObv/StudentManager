<script>
// 门禁卡管理组件
export default {
  name: 'CardIDManage',
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
  max-width: 1200px;
  margin: 0 auto;
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