<script>
import HeaderComp from '@/components/TeacherComp/HeaderComp.vue'
import MyStudents from '@/components/TeacherComp/Mystudents.vue'
export default {
  name: 'TeachersPage',
  data() {
    return {
      options:null,                             // 头部导航栏选项
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
    HeaderComp,                             // 老师头部导航
    MyStudents,                             // 我的学生
  }
}
</script>

<template>
  <div>
    <HeaderComp @update-option="handleHeaderClick"></HeaderComp>
    <h1 v-if="this.options === 0">宿舍申请</h1>
    <h1 v-if="this.options === 1">我的宿舍</h1>
    <MyStudents v-if="this.options === 2"></MyStudents>
    <h1 v-if="this.options === 3">宿舍分配</h1>
  </div>
</template>

<style scoped>

</style>