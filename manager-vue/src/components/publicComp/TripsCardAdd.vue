<script>
// 添加门禁卡组件
export default {
  name: 'TripsCardAdd',
  data() {
    return {
      // {
      //   number: 门禁卡号,
      //   student: 关联的学生,
      // }
      tripsCards: [],                                                                    // 门禁卡列表
    }
  },
  created() {
    this.loadLocalData();
  },
  watch: {
    tripsCards: {
      handler() {
        this.saveLocalData();
      },
      deep: true
    }
  },
  methods: {
    loadLocalData() {                                                                    // 从本地存储加载数据
      try {
        const cachedData = localStorage.getItem('TripsCardsCach');
        if (cachedData) {
          this.tripsCards = JSON.parse(cachedData);
        }
      } catch (error) {
        console.error('加载本地数据失败:', error);
        this.tripsCards = [];
      }
    },
    saveLocalData() {                                                                    // 保存数据到本地存储
      try {
        localStorage.setItem('TripsCardsCach', JSON.stringify(this.tripsCards));
      } catch (error) {
        console.error('保存本地数据失败:', error);
      }
    },
    addNewRow() {                                                                       // 添加新行
      this.tripsCards.push({ number: '', student: '' });
    },
    removeRow(index) {                                                                   // 移除行
      this.tripsCards.splice(index, 1);
    },
    clearData() {                                                                       // 清除所有数据
      if (confirm('确定要清除所有数据吗？')) {
        this.tripsCards = [];
        localStorage.removeItem('TripsCardsCach');
      }
    },
    sendData() {                                                                        // 发送数据请求
      if (this.tripsCards.length === 0) {
        alert('没有数据可以发送');
        return;
      }
      // 模拟请求
      console.log('发送数据:', this.tripsCards);
      // 模拟请求成功
      setTimeout(() => {
        alert('数据发送成功！');
        // 清除本地数据
        this.tripsCards = [];
        localStorage.removeItem('TripsCardsCach');
      }, 1000);
    },
    handleInputChange(index, field, value) {                                            // 处理输入变化
      this.tripsCards[index][field] = value;
    }
  }
}
</script>


<template>
  <div class="trips-card-add">
    <!-- 操作按钮 -->
    <div class="action-buttons">
      <button class="btn btn-clear" @click="clearData">
        <span class="btn-icon">🗑️</span>
        清除数据
      </button>
      <button class="btn btn-send" @click="sendData">
        <span class="btn-icon">📤</span>
        发送数据
      </button>
    </div>
    
    <!-- 表格 -->
    <div class="table-container">
      <table class="trips-table">
        <thead>
          <tr>
            <th>门禁卡号</th>
            <th>关联学生</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(card, index) in tripsCards" :key="index">
            <td>
              <input 
                type="text" 
                v-model="card.number" 
                @input="handleInputChange(index, 'number', card.number)"
                placeholder="请输入门禁卡号"
                class="input-field"
              />
            </td>
            <td>
              <input 
                type="text" 
                v-model="card.student" 
                @input="handleInputChange(index, 'student', card.student)"
                placeholder="请输入关联学生"
                class="input-field"
              />
            </td>
            <td>
              <button class="btn btn-remove" @click="removeRow(index)">
                <span class="btn-icon">❌</span>
                删除
              </button>
            </td>
          </tr>
          <!-- 添加按钮行 -->
          <tr>
            <td colspan="3">
              <button class="btn btn-add" @click="addNewRow">
                <span class="btn-icon">➕</span>
                添加门禁卡
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<style scoped>
.trips-card-add {
  padding: 20px;
  background: transparent;
  border-radius: 12px;
  box-shadow: none;
  border: none;
  width: 100%;
  margin: 0;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  justify-content: flex-start;
}

.btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-clear {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.btn-clear:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
}

.btn-send {
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
}

.btn-send:hover {
  background: linear-gradient(135deg, #059669, #047857);
}

.btn-add {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  width: 100%;
  justify-content: center;
  margin: 10px 0;
}

.btn-add:hover {
  background: linear-gradient(135deg, #2563eb, #1e40af);
}

.btn-remove {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  padding: 6px 12px;
  font-size: 12px;
}

.btn-remove:hover {
  background: linear-gradient(135deg, #dc2626, #b91c1c);
}

.btn-icon {
  font-size: 14px;
}

/* 表格 */
.table-container {
  width: 100%;
  overflow-x: auto;
}

.trips-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.trips-table th,
.trips-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.trips-table th {
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  font-weight: 600;
  color: #1e293b;
  font-size: 14px;
}

.trips-table tr:hover {
  background: #f8fafc;
}

.input-field {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .trips-card-add {
    padding: 16px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .trips-table th,
  .trips-table td {
    padding: 10px 12px;
  }
}
</style>