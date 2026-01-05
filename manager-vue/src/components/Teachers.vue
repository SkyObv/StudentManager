<script>
import HeaderComp from '@/components/TeacherComp/HeaderComp.vue'
import MyStudents from '@/components/TeacherComp/Mystudents.vue'
import ApplyHostelLogs from '@/components/TeacherComp/ApplyHostelLogs.vue'
import ApplyHostel from '@/components/TeacherComp/ApplyHostel.vue'
export default {
  name: 'TeachersPage',
  data() {
    return {
      options:0,                             // 头部导航栏选项
    }
  },
  methods: {
    // 处理老师头部导航栏点击事件
    handleHeaderClick(options) {
      console.log(options)
      this.options = options
    }
  },
  components: {
    ApplyHostel,                            // 申请宿舍
    ApplyHostelLogs,                        // 申请记录
    HeaderComp,                             // 老师头部导航
    MyStudents,                             // 我的学生
  }
}
</script>

<template>
  <div>
    <HeaderComp @update-option="handleHeaderClick"></HeaderComp>
    <ApplyHostel v-if="this.options === 0">宿舍申请</ApplyHostel>
    <ApplyHostelLogs  v-if="this.options === 1">申请记录</ApplyHostelLogs >
    <h1 v-if="this.options === 2">我的宿舍</h1>
    <MyStudents v-if="this.options === 3"></MyStudents>
    <h1 v-if="this.options === 4">宿舍分配</h1>
  </div>
</template>

<style scoped>

</style>