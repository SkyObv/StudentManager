<script>
import HeaderComp from '@/components/TeacherComp/HeaderComp.vue'
import MyStudents from '@/components/TeacherComp/Mystudents.vue'
import ApplyHostelLogs from '@/components/TeacherComp/ApplyHostelLogs.vue'
import ApplyHostel from '@/components/TeacherComp/ApplyHostel.vue'
import MyHostels from "@/components/TeacherComp/MyHostels.vue";
import CardIDManage from "@/components/TeacherComp/CardIDManage.vue";  // 门禁卡管理
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
    MyHostels,                              // 我的宿舍
    MyStudents,                             // 我的学生
    CardIDManage,                           // 门禁卡管理
  }
}
</script>

<template>
  <div>
    <HeaderComp @update-option="handleHeaderClick"></HeaderComp>
    <ApplyHostel v-if="this.options === 0">宿舍申请</ApplyHostel>
    <ApplyHostelLogs  v-if="this.options === 1">申请记录</ApplyHostelLogs >
    <MyHostels v-if="this.options === 2">我的宿舍</MyHostels>
    <MyStudents v-if="this.options === 3"></MyStudents>
    <CardIDManage v-if="this.options === 4">门禁卡管理</CardIDManage>
  </div>
</template>

<style scoped>

</style>