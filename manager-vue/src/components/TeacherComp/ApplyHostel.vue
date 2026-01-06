<script>
import ApplyHostelCard from "@/components/publicComp/ApplyHostelCard.vue";
export default {
  components: {
    ApplyHostelCard                               // 宿舍信息卡片
  },
  data() {
    return {
      hostelList: [],        // 当前宿舍数据
      count_hostel : 1,      //宿舍统计数据
      searchKeyword : null,
      buildingNumber: 1,   // 当前宿舍所属楼号，默认是1号楼
      floors: []           // 楼号数据列表
    }
  },
  created() {
    this.getFloor()                                                            // 获取楼层数据
    this.getHostel()
  },
  methods: {
    getFloor(){ // 获取楼号数据
      this.$axios.get(`${this.$settings.Host}/users/floors/`).then(response => {
      this.floors = response.data;
      console.log(this.floors)
    }).catch(error => {
      console.log(error);
      this.$message.error("楼层数据获取失败！")
    })
    },

    getHostel(){ // 获取当前楼号的宿舍数据
      this.$axios.get(`${this.$settings.Host}/teacher/get/hostel/?floor=${this.buildingNumber}`).then(response => {
        this.hostelList = response.data
        this.count_hostel = this.hostelList.length
      }).catch(error => {
        console.log(error);
        this.$message.error("宿舍数据获取失败！")
      })
    },

    changeFool(){
      this.getHostel()    // 重新获取楼层的宿舍信息数据
    }
  },
}
</script>

<template>
  <div class="apply-hostel-container">
    <div class="apply-hostel-header">
      <h2 class="page-title">宿舍申请</h2>
      <!-- 楼号标题 -->
      <h3 class="building-title">{{ buildingNumber }}号楼</h3>
      <!-- 楼号下拉选择 -->
      <div class="search-container">
        <select 
          v-model="buildingNumber" 
          class="search-input"
          @change="changeFool"
        >
          <option 
            v-for="floor in floors"
            :key="floor.floor_name"
            :value="floor.floor_name"
          >
            {{ floor.floor_name }}号楼
          </option>
        </select>
      </div>
      <!-- 宿舍数量提示 -->
      <h3 class="building-title">共有 {{ count_hostel }} 宿舍可申请</h3>
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
  margin-bottom: 0.5rem;
  animation: fadeInUp 0.8s ease-out;
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 楼号标题 */
.building-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0.5rem 0 1.5rem 0;
  animation: fadeInUp 0.8s ease-out 0.1s both;
}

/* 搜索容器 */
.search-container {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  gap: 8px;
}

/* 搜索输入框 */
.search-input {
  flex: 1;
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

/* 搜索按钮 */
.search-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.search-button:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

.search-icon {
  font-size: 16px;
}

.search-text {
  font-size: 14px;
  font-weight: 500;
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

/* 下拉框特定样式 */
.search-input {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12' fill='none'%3E%3Cpath d='M6 9L1 4L11 4L6 9Z' fill='%236B7280'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 12px;
  cursor: pointer;
  padding-right: 2.5rem;
}

.search-input::-ms-expand {
  display: none;
}

/* 下拉框选项样式 */
.search-input option {
  background-color: white;
  color: #374151;
  padding: 0.5rem;
  font-weight: 500;
}

.search-input option:hover {
  background-color: #f3f4f6;
}

.search-input:hover {
  border-color: #93c5fd;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
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