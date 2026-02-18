<script>
import HostelInfoCard from "@/components/publicComp/HostelInfoCard.vue";

// 我的宿舍页面
export default {
  name  : "MyHostels",
  components: {
    HostelInfoCard,
  },
  data () {
    return {
      hostelinfo : [],                                               // 宿舍卡片信息数据
      floors: [],                                                    // 楼号数据
      myStudents: [],                                                // 我的学生的数据

      selectedFloor: null,                                           // 选中的楼层
      gender: null,                                                  // 选中的性别 
      showMyStudents: false,                                         // 是否显示我的学生
    }
  },
  created() {
    this.getAllFloors()                                              // 获取所有楼号
    this.getHostels()                                                // 获取所有宿舍
    this.getStudents()                                               // 获取所有学生
  },
  methods : {
    // 添加学生
    addStudent () {
      alert('添加学生')
    },
    // 删除学生
    deleteStudent (student) {
      alert(`删除学生 ： ${student.name}`)
    },
    getAllFloors(){                                                  // 获取所有楼层数据
      this.$axios.get(`${this.$settings.Host}/users/floors/`).then(res => {
        this.selectedFloor = res.data[0].id
        this.floors = res.data
      }).catch(error=>{
        console.log(error);
        this.$message.error("楼层数据获取失败！")
      })
    },
    getHostels(){                                                    // 获取单独楼层宿舍数据
      let params = {}                                                // 请求参数
      if(this.selectedFloor){params.floor = this.selectedFloor}
      if(this.gender){params.gender = this.gender}
      this.$axios(
        {
          url: `${this.$settings.Host}/teacher/myhostel/allget/`,
          method: 'get',
          params: params,
          headers: {
            Authorization: `Hander ${this.$settings.getToken()}`
          }
        }
      ).then(res => {
        this.hostelinfo = res.data
      }).catch(error=>{
        console.log(error);
        this.$message.error("宿舍数据获取失败！")
        }
      )
    },
    getStudents(){                                                   // 获取我的学生
      let params = {is_hostel:false}
      if (this.gender){params.gender = this.gender}
      this.$axios({
        url: `${this.$settings.Host}/teacher/get/allStudents/`,
        method: 'get',
        params: params,
        headers: {
          Authorization: `Hander ${this.$settings.getToken()}`
        }
      }).then(res => {
        this.myStudents = res.data
      }).catch(error=>{
        console.log(error);
        this.$message.error("学生数据获取失败！")
        }
      )
    },
    refreshData() {                                                  // 刷新数据
      this.getHostels()
      this.getStudents()
    },
  }
}
</script>

<template>
  <div class="my-hostels-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">我的宿舍管理</h1>
      
      <!-- 楼号选择下拉框和我的学生按钮 -->
      <div class="floor-selector-container">
        <div class="floor-selector">
          <label for="floor-select">选择楼层：</label>
          <select id="floor-select" v-model="selectedFloor" class="floor-select" @change="refreshData">
            <option value="">全部楼层</option>
            <option v-for="floor in floors" :key="floor.id" :value="floor.id">
              {{ floor.floor_name}}号楼
            </option>
          </select>
          
          <!-- 性别筛选下拉框 -->
          <label for="gender-select">选择性别：</label>
          <select id="gender-select" v-model="gender" class="gender-select" @change="refreshData">
            <option :value="null">全部性别</option>
            <option value="male">男生</option>
            <option value="female">女生</option>
          </select>
          
          <!-- 我的学生按钮 -->
          <button class="my-students-button" @click="showMyStudents = !showMyStudents">
            <span class="button-icon">👥</span>
            我的学生
          </button>
        </div>
      </div>
    </div>
    
    <!-- 主内容区域 -->
    <div class="main-content" :class="{ 'with-students': showMyStudents }">
      <!-- 宿舍卡片网格 -->
      <div class="hostels-grid">
        <HostelInfoCard
          v-for="hostel in hostelinfo"
          :key="hostel.id"
          :hostel="hostel"
          @addStudent="addStudent"
          @deleteStudent="deleteStudent"
        >
        </HostelInfoCard>
        
        <!-- 无数据提示 -->
        <div class="no-data" v-if="hostelinfo.length === 0">
          <p>暂无管理的宿舍</p>
        </div>
      </div>
      
      <!-- 我的学生列表 -->
      <div class="my-students-section" v-if="showMyStudents">
        <div class="section-header">
          <h3 class="section-title">我的学生</h3>
        </div>
        <div class="students-list-vertical">
          <div class="student-item" v-for="student in myStudents" :key="student.id">
            <span class="student-name">{{ student.name }}</span>
            <span class="student-gender" :class="student.gender">
              {{ student.gender === 'male' ? '♂' : '♀' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.my-hostels-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 页面头部 */
.page-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
  animation: fadeInDown 0.6s ease-out;
  width: 100%;
}

/* 页面标题 */
.page-title {
  color: #1e293b;
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.5px;
  animation: slideInUp 0.8s ease-out 0.2s both;
  margin-bottom: 15px;
  text-align: center;
  width: 100%;
}

/* 楼号选择器容器 */
.floor-selector-container {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  animation: fadeIn 1s ease-out 0.4s both;
}

/* 楼号选择器 */
.floor-selector {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 15px;
}

.floor-selector label {
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  white-space: nowrap;
}

.floor-select {
  padding: 8px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  background: white;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  min-width: 120px;
}

.floor-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* 性别选择下拉框 */
.gender-select {
  padding: 8px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  background: white;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  min-width: 120px;
}

.gender-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* 我的学生按钮 */
.my-students-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
  min-width: 120px;
  justify-content: center;
  line-height: 20px;
  min-height: 40px;
}

.my-students-button:hover {
  background: linear-gradient(135deg, #059669, #047857);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
}

.button-icon {
  font-size: 14px;
}

/* 主内容区域 */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 25px;
  animation: fadeIn 1s ease-out 0.4s both;
}

/* 显示学生列表时的布局 */
.main-content.with-students {
  flex-direction: row;
  align-items: flex-start;
}

.main-content.with-students .hostels-grid {
  flex: 2;
  min-width: 0;
}

/* 我的学生列表区域 */
.my-students-section {
  flex: 1;
  min-width: 250px;
  background: linear-gradient(135deg, #ffffff, #f8fafc);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  animation: slideInRight 0.8s ease-out;
}

/* 学生列表标题 */
.section-header {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #f1f5f9;
}

.section-header .section-title {
  font-size: 18px;
  font-weight: 700;
  color: #374151;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-header .section-title::before {
  content: "👥";
  font-size: 16px;
}

/* 纵向学生列表 */
.students-list-vertical {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* 学生项样式 */
.students-list-vertical .student-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  background: linear-gradient(135deg, #ffffff, #f8fafc);
  border-radius: 12px;
  font-size: 14px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.students-list-vertical .student-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
  border-color: #3b82f6;
}

.students-list-vertical .student-name {
  color: #1e293b;
  font-weight: 600;
  flex: 1;
}

.students-list-vertical .student-gender {
  font-size: 16px;
  font-weight: bold;
}

.students-list-vertical .student-gender.male {
  color: #3b82f6;
}

.students-list-vertical .student-gender.female {
  color: #db2777;
}

/* 动画效果 */
@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 宿舍卡片网格 */
.hostels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
  animation: fadeIn 1s ease-out 0.4s both;
}

/* 无数据提示 */
.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #94a3b8;
  background: linear-gradient(135deg, #f8fafc, #ffffff);
  border-radius: 16px;
  border: 2px dashed #cbd5e1;
  margin-bottom: 30px;
  transition: all 0.3s ease;
  animation: fadeIn 1s ease-out 0.4s both;
}

.no-data:hover {
  border-color: #94a3b8;
  background: #f1f5f9;
}

.no-data p {
  font-size: 16px;
  font-weight: 500;
  margin: 0;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInUp {
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
@media (max-width: 767px) {
  .my-hostels-container {
    padding: 15px;
  }
  
  .page-header {
    padding-bottom: 15px;
  }
  
  .page-title {
    font-size: 24px;
  }
  
  /* 楼号选择器响应式 */
  .floor-selector {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    width: 100%;
  }
  
  .floor-select {
    width: 100%;
    min-width: unset;
  }
  
  .gender-select {
    width: 100%;
    min-width: unset;
  }
  
  .my-students-button {
    width: 100%;
    min-width: unset;
  }
  
  /* 显示学生列表时的响应式布局 */
  .main-content.with-students {
    flex-direction: column;
  }
  
  .my-students-section {
    min-width: unset;
  }
  
  .hostels-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>