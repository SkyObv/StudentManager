<script>
export default {
  name: 'FloorManage',
  data() {
    return {
      // 用户数据
      token:sessionStorage.getItem('token') || localStorage.getItem('token'),
      refresh:sessionStorage.getItem('refresh') || localStorage.getItem('refresh'),
      // 楼层数据
      floors:[],
      // 动画状态
      animateBuilding: false,
      // 房间使用状态（随机生成灯光效果）
      roomLights: {},
      // 创建楼层相关
      showCreateModal: false,
      newFloor: {
        floor_name: ''
      },
      // 删除楼层对话框相关数据
      showDeleteFloorForm: false,
      selectedFloor: null
    }
  },
  created() {
    // 获取楼层数据
    this.$axios.get(`${this.$settings.Host}/users/floors/`).then(response => {
      this.floors = response.data;
    }).catch(error => {
      console.log(error);
      this.$message.error("楼层数据获取失败！")
    })
  },
  computed: {
    // 计算每个楼层的空闲房间数
    getAvailableRooms() {
      return (floor) => {
        return floor.rooms - floor.have_people_rooms;
      };
    },
    // 计算占用百分比
    getOccupancyRate() {
      return (floor) => {
        return Math.round((floor.have_people_rooms / floor.rooms) * 100);
      };
    },
    // 获取状态颜色
    getStatusColor() {
      return (rate) => {
        if (rate > 80) return '#ef4444'; // 红色 - 高占用
        if (rate > 60) return '#f97316'; // 橙色 - 中高占用
        if (rate > 40) return '#eab308'; // 黄色 - 中等占用
        return '#22c55e'; // 绿色 - 低占用
      };
    }
  },
  methods: {
    // 点击楼层卡片的处理函数
    handleFloorClick(floorID) {
      this.$emit('FloorClick', floorID)
      // 添加点击动画效果
      this.animateBuilding = true;
      setTimeout(() => {
        this.animateBuilding = false;
      }, 300);
      // 这里可以添加跳转到该楼层详情页的逻辑
    },
    // 检查房间是否亮灯（默认固定状态）
    isRoomLit(floorName, floorNum, roomNum) {
        // 使用简单的数学模式生成固定的灯光效果
        // 确保每栋楼的灯光模式一致且有规律
        // 将楼层名称转换为数字进行计算
        const floorId = parseInt(floorName);
        return (floorId + floorNum + roomNum) % 2 === 0;
      },
    // 创建新楼层
    showCreateFloorModal() {
      // 重置表单
      this.newFloor = {
        floor_name: ''
      };
      this.showCreateModal = true;
    },
    // 确认创建楼层
    createFloor() {
      if (!this.newFloor.floor_name.trim()) {
        this.$message.warning('请输入楼层名称');
        return;
      }
      // 检查名称是否已存在
      if (this.floors.some(floor => floor.floor_name === this.newFloor.floor_name)) {
        this.$message.warning('该楼层名称已存在');
        return;
      }
      // 创建新楼层，设置默认值
      const newFloor = {
        floor_name: this.newFloor.floor_name,
      };
      // 发送请求创建楼层
      this.$axios.post(`${this.$settings.Host}/users/create/floor/`, newFloor).then(response => {
        this.$message.success(response.data.message)
        window.location.reload()
      }).catch(err=>{
        console.log(err)
        this.$message.error(err.response.data.message)
      })
    
      // 关闭模态框
      this.showCreateModal = false;
  },
    // 打开删除楼层对话框
    openDeleteFloorForm(floor) {
      this.selectedFloor = floor;
      this.showDeleteFloorForm = true;
    },
    
    // 关闭删除楼层对话框
    closeDeleteFloorForm() {
      this.showDeleteFloorForm = false;
      this.selectedFloor = null;
    },
    
    // 确认删除楼层
    confirmDeleteFloor() {
      if (!this.selectedFloor) return;
      
      // 发送删除请求
      console.log('删除楼层:', this.selectedFloor.id);
      this.$axios.delete(`${this.$settings.Host}/users/delete/${this.selectedFloor.id}/floor`)
        .then(response => {
          this.$message.success(response.data.message);
          // 重新加载楼层数据
          this.$axios.get(`${this.$settings.Host}/users/floors/`).then(res => {
            this.floors = res.data;
          });
          // 关闭对话框
          this.closeDeleteFloorForm();
        })
        .catch(err => {
          console.log(err);
          this.$message.error('删除失败！');
        });
    }
  },
  mounted() {
    // 页面加载完成后添加动画效果
    setTimeout(() => {
      this.pageLoaded = true;
    }, 100);
  }
}
</script>

<template>
  <div class="floor-manage">
    <!-- 现代化的标题栏 -->
    <div class="page-header">
      <h1 class="page-title">楼层管理</h1>
      <p class="page-subtitle">查看和管理所有宿舍楼层信息</p>
    </div>
    
    <!-- 操作按钮区域 -->
    <div class="action-buttons">
      <button class="create-button" @click="showCreateFloorModal">
        <svg class="button-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        创建楼层
      </button>
    </div>
    
    <!-- 楼层卡片布局 -->
    <div class="floor-grid">
      <div 
        v-for="floor in floors" 
        :key="floor.floor_name"
        class="floor-card"
        @click="handleFloorClick(floor.id)"
      >
        <!-- 卡片头部 -->
        <div class="card-header">
          <h3 class="floor-name">{{ floor.floor_name }}号楼</h3>
          <div class="floor-status" :style="{ backgroundColor: getStatusColor(getOccupancyRate(floor)) }">
            {{ getOccupancyRate(floor) > 80 ? '已满' : getOccupancyRate(floor) > 60 ? '紧张' : getOccupancyRate(floor) > 40 ? '适中' : '充足' }}
          </div>
        </div>
        
        <!-- 楼房样式图片（重新设计的3D效果） -->
        <div class="building-container" :class="{ 'animate-building': animateBuilding }">
          <div class="building">
            <!-- 屋顶 -->
            <div class="roof"></div>
            <!-- 楼层 -->
            <div class="floor-level" v-for="i in 5" :key="i">
              <div 
                class="window" 
                v-for="j in 3" 
                :key="j"
                :class="{ 'lit': isRoomLit(floor.floor_name, i, j) }"
              ></div>
            </div>
            <!-- 门 -->
            <div class="door"></div>
          </div>
          <!-- 装饰性元素 -->
          <div class="ground"></div>
          <div class="shadow"></div>
        </div>
        
        <!-- 占用率进度条 -->
        <div class="occupancy-section">
          <div class="progress-label">
            <span>占用率</span>
            <span>{{ getOccupancyRate(floor) }}%</span>
          </div>
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ 
                width: `${getOccupancyRate(floor)}%`,
                backgroundColor: getStatusColor(getOccupancyRate(floor)) 
              }"
            ></div>
          </div>
        </div>
        
        <!-- 房间统计信息 -->
        <div class="stats-container">
          <div class="stat-item">
            <div class="stat-value total">{{ floor.rooms }}</div>
            <div class="stat-label">总房间</div>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <div class="stat-value occupied">{{ floor.have_people_rooms }}</div>
            <div class="stat-label">已占用</div>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <div class="stat-value available">{{ getAvailableRooms(floor) }}</div>
            <div class="stat-label">空闲</div>
          </div>
        </div>
        
        <!-- 操作按钮区域 -->
        <div class="card-actions">
          <button class="detail-button">
            查看详情
            <svg class="arrow-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </button>
          <button class="delete-button" @click.stop="openDeleteFloorForm(floor)">
            <svg class="button-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              <line x1="10" y1="11" x2="10" y2="17"></line>
              <line x1="14" y1="11" x2="14" y2="17"></line>
            </svg>
            删除
          </button>
        </div>
      </div>
    </div>
    
    <!-- 创建楼层模态框 -->
    <div v-if="showCreateModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h3>创建新楼层</h3>
          <button class="close-button" @click="showCreateModal = false">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="floorName">楼层名称</label>
            <input 
              type="text" 
              id="floorName" 
              v-model="newFloor.floor_name"
              placeholder="如：7"
              class="form-input"
            >
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-button" @click="showCreateModal = false">取消</button>
          <button class="confirm-button" @click="createFloor">创建</button>
        </div>
      </div>
    </div>
    
    <!-- 删除楼层对话框 -->
    <div class="modal" v-if="showDeleteFloorForm">
      <div class="modal-content">
        <div class="modal-header">
          <h3>删除楼层</h3>
          <button class="close-button" @click="closeDeleteFloorForm">×</button>
        </div>
        <div class="modal-body">
          <div class="delete-confirm">
            <p>确定要删除楼层 <strong>{{ selectedFloor?.floor_name }}</strong> 吗？</p>
            <p class="delete-warning">删除后该楼层下的所有宿舍信息也将被删除，此操作不可恢复，请谨慎操作。</p>
          </div>
          <div class="form-actions">
            <button type="button" class="cancel-button" @click="closeDeleteFloorForm">取消</button>
            <button type="button" class="delete-confirm-button" @click="confirmDeleteFloor">确认删除</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 重置和基础样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.floor-manage {
  padding: 2rem;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  min-height: 100vh;
  color: #333;
  animation: pageFadeIn 0.6s ease-out;
}

/* 页面标题 */
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

/* 楼层卡片网格布局 */
.floor-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: modalSlideIn 0.3s ease;
}

@keyframes modalSlideIn {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
}

.modal-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #94a3b8;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.close-button:hover {
  color: #64748b;
  background: #f1f5f9;
}

.modal-body {
  padding: 1.5rem;
}

.delete-confirm p {
  margin-bottom: 1rem;
  color: #374151;
  font-size: 1rem;
}

.delete-warning {
  color: #ef4444;
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.cancel-button {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-button:hover {
  background: #e5e7eb;
  transform: translateY(-1px);
}

.delete-confirm-button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.delete-confirm-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
}

/* 操作按钮区域 */
.action-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.create-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
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

.create-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
}

.create-button:active {
  transform: translateY(0);
}

.button-icon {
  transition: transform 0.3s ease;
}

.create-button:hover .button-icon {
  transform: rotate(90deg);
}

/* 楼层卡片 */
.floor-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid #f1f5f9;
}

.floor-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.floor-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.floor-card:hover::before {
  transform: scaleX(1);
}

.floor-card:active {
  transform: translateY(-4px);
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.floor-name {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.floor-status {
  padding: 0.3rem 0.8rem;
  border-radius: 1rem;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 楼房容器 */
.building-container {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 180px;
  margin-bottom: 1.5rem;
  position: relative;
  perspective: 1000px;
}

/* 建筑物 */
.building {
  width: 80px;
  height: 120px;
  background: linear-gradient(to bottom, #f8fafc, #e2e8f0);
  border: 2px solid #3b82f6;
  border-radius: 4px 4px 0 0;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.3s ease;
  z-index: 2;
}

.floor-card:hover .building {
  transform: translateY(-5px) rotateX(5deg);
}

/* 屋顶 */
.roof {
  width: 0;
  height: 0;
  border-left: 42px solid transparent;
  border-right: 42px solid transparent;
  border-bottom: 20px solid #3b82f6;
  position: absolute;
  top: -20px;
  left: -2px;
  transform-origin: center;
  transition: transform 0.3s ease;
}

.floor-card:hover .roof {
  transform: translateY(-2px);
}

/* 楼层 */
.floor-level {
  height: 20px;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 0 8px;
  position: relative;
  margin-top: 2px;
}

.floor-level::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 8px;
  right: 8px;
  height: 1px;
  background: rgba(0, 0, 0, 0.05);
}

/* 窗户 */
.window {
  width: 12px;
  height: 12px;
  background: #e0f2fe;
  border-radius: 2px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.3s ease;
  animation: windowPulse 3s ease-in-out infinite;
}

.window::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 1px;
  background: rgba(0, 0, 0, 0.1);
}

.window::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1px;
  height: 100%;
  background: rgba(0, 0, 0, 0.1);
}

.window.lit {
  background: linear-gradient(45deg, #ffeb3b, #ffc107);
  box-shadow: 
    inset 0 1px 3px rgba(0, 0, 0, 0.1),
    0 0 8px rgba(255, 235, 59, 0.7);
  animation: windowGlow 2s ease-in-out infinite alternate;
}

/* 门 */
.door {
  width: 16px;
  height: 24px;
  background: linear-gradient(to bottom, #8b4513, #654321);
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 2px 2px 0 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.door::before {
  content: '';
  position: absolute;
  top: 8px;
  right: 3px;
  width: 2px;
  height: 2px;
  background: #ffc107;
  border-radius: 50%;
  box-shadow: 0 0 2px rgba(255, 193, 7, 0.8);
}

/* 地面和阴影 */
.ground {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 10px;
  background: linear-gradient(to top, #d1d5db, transparent);
  border-radius: 50% 50% 0 0;
  z-index: 1;
}

.shadow {
  position: absolute;
  bottom: 5px;
  width: 90px;
  height: 8px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  z-index: 0;
  transform: scaleX(0.8);
  transition: all 0.3s ease;
}

.floor-card:hover .shadow {
  transform: scaleX(1);
}

/* 占用率部分 */
.occupancy-section {
  margin-bottom: 1.5rem;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: #64748b;
  font-weight: 500;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
  position: relative;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: progressShine 2s ease-in-out infinite;
}

/* 统计信息 */
.stats-container {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1rem;
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-divider {
  width: 1px;
  background: #e2e8f0;
  margin: 0 1rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.stat-value.total {
  color: #3b82f6;
}

.stat-value.occupied {
  color: #ef4444;
}

.stat-value.available {
  color: #22c55e;
}

.stat-label {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

/* 详情按钮 */
.detail-button {
  width: 100%;
  padding: 0.75rem 1rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  filter: brightness(1.05);
}

.detail-button:active {
  transform: translateY(0);
}

.arrow-icon {
  transition: transform 0.3s ease;
}

.detail-button:hover .arrow-icon {
  transform: translateX(3px);
}

/* 卡片操作按钮 */
.card-actions {
  display: flex;
  gap: 0.5rem;
}

.delete-button {
  flex: 1;
  padding: 0.75rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.delete-button:hover {
  background: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.delete-button:active {
  transform: translateY(0);
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  padding: 0;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1f2937;
}

.close-button {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.25rem;
  transition: all 0.2s ease;
}

.close-button:hover {
  background: #f3f4f6;
  color: #374151;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05);
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.cancel-button {
  padding: 0.75rem 1.5rem;
  background: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-button:hover {
  background: #e5e7eb;
}

.confirm-button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.confirm-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.confirm-button:active {
  transform: translateY(0);
}

/* 页面加载动画 */
@keyframes pageFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
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

@keyframes buildingPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
}

@keyframes windowPulse {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 1; }
}

@keyframes windowGlow {
  0% { box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 4px rgba(255, 235, 59, 0.5); }
  100% { box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 12px rgba(255, 235, 59, 0.8); }
}

@keyframes progressShine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* 建筑物动画 */
.animate-building {
  animation: buildingPulse 0.6s ease-in-out;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .floor-manage {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .page-subtitle {
    font-size: 1rem;
  }
  
  .floor-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .floor-card {
    padding: 1.25rem;
  }
  
  .stats-container {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }
  
  .stat-divider {
    width: 100%;
    height: 1px;
    margin: 0;
  }
  
  .stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    text-align: left;
  }
  
  .stat-label {
    text-align: right;
  }
  
  /* 移动端操作按钮 */
  .card-actions {
    flex-direction: column;
  }
  
  .create-button {
    width: 100%;
    justify-content: center;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1.25rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }
  
  .floor-card {
    padding: 1rem;
  }
  
  .building-container {
    height: 150px;
  }
  
  .building {
    width: 70px;
    height: 100px;
  }
  
  .roof {
    border-left: 37px solid transparent;
    border-right: 37px solid transparent;
    border-bottom: 15px solid;
    top: -15px;
  }
  
  .action-buttons {
    padding: 0 1rem;
  }
}
</style>