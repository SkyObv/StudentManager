<script>
// 选择学生组件：创建时拉取教师名下全部学生，单选后点确定把 studentId 交给父组件
export default {
  name: 'StudentSelect',
  props: {
    /** 当前要绑定的门禁卡 id，仅用于标题展示 */
    cardId: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      students: [],
      loading: false,
      selectedId: null
    }
  },
  created() {
    this.fetchStudents()                                                                 // 创建时拉取教师名下全部学生
  },
  methods: {
    fetchStudents() {                                                                    // http请求获取全部学生列表
      this.loading = true
      this.$axios({
        url: `${this.$settings.Host}/teacher/get/allStudents/`,
        method: 'get',
        params: {
          "key":false
        },
        headers: {
          Authorization: `Hander ${this.$settings.getToken()}`
        }
      })
        .then(res => {
          this.students = Array.isArray(res.data) ? res.data : []
        })
        .catch(err => {
          console.error(err)
          this.$message.error('获取学生列表失败')
          this.students = []
        })
        .finally(() => {
          this.loading = false
        })
    },
    onConfirm() {                                                                        // 校验选择并向父组件提交 studentId
      if (this.selectedId == null || this.selectedId === '') {
        this.$message.warning('请先选择一名学生')
        return
      }
      const id = Number(this.selectedId)
      this.$emit('confirm', id)
      this.selectedId = null
    },
    onCancel() {                                                                         // 取消选择并通知父组件关闭
      this.selectedId = null
      this.$emit('cancel')
    }
  }
}
</script>

<template>
  <div class="student-select-mask" @click.self="onCancel">
    <div class="student-select-panel" @click.stop>
      <div class="panel-header">
        <h3 class="panel-title">选择要绑定的学生</h3>
        <p v-if="cardId != null && !Number.isNaN(cardId)" class="panel-sub">
          门禁卡 ID：{{ cardId }}
        </p>
      </div>

      <div v-loading="loading" class="panel-body">
        <p v-if="!loading && students.length === 0" class="empty-tip">暂无学生数据</p>
        <el-radio-group v-else v-model="selectedId" class="radio-list">
          <el-radio
            v-for="s in students"
            :key="s.id"
            :label="s.id"
            class="radio-item"
          >
            <span class="student-line">
              <span class="name">{{ s.name || '未命名' }}</span>
              <span class="meta">学号 {{ s.username }}</span>
              <span
                class="gender"
                :class="s.gender === 'male' ? 'male' : 'female'"
              >{{ s.gender === 'male' ? '男' : '女' }}</span>
            </span>
          </el-radio>
        </el-radio-group>
      </div>

      <div class="panel-footer">
        <el-button size="medium" @click="onCancel">取消</el-button>
        <el-button type="primary" size="medium" @click="onConfirm">确定</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.student-select-mask {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.student-select-panel {
  width: 100%;
  max-width: 420px;
  max-height: 85vh;
  background: linear-gradient(180deg, #fff 0%, #f8fafc 100%);
  border-radius: 16px;
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: 20px 20px 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.panel-title {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
}

.panel-sub {
  margin: 8px 0 0;
  font-size: 13px;
  color: #64748b;
}

.panel-body {
  padding: 16px 20px;
  min-height: 0;                                                                       /* flex 子项可收缩，保证内部 overflow 能滚动 */
  flex: 1 1 auto;                                                                      /* 占满标题与底部之间的剩余高度 */
  max-height: 50vh;                                                                     /* 列表过长时在此区域纵向滚动，50 人可全部列出 */
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.empty-tip {
  text-align: center;
  color: #94a3b8;
  margin: 24px 0;
  font-size: 14px;
}

.radio-list {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  width: 100%;
}

.radio-item {
  margin: 0 0 10px !important;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(226, 232, 240, 0.9);
  transition: border-color 0.2s, box-shadow 0.2s;
  height: auto;
  line-height: 1.5;
  white-space: normal;
}

.radio-item:hover {
  border-color: #93c5fd;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.12);
}

.student-line {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 12px;
  margin-left: 4px;
}

.student-line .name {
  font-weight: 600;
  color: #334155;
}

.student-line .meta {
  font-size: 12px;
  color: #64748b;
}

.student-line .gender {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 6px;
}

.student-line .gender.male {
  background: #dbeafe;
  color: #1d4ed8;
}

.student-line .gender.female {
  background: #fce7f3;
  color: #be185d;
}

.panel-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 20px;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(248, 250, 252, 0.8);
}
</style>
