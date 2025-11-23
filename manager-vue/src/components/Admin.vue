<script>
import HanderComp from "@/components/AdminComp/HanderComp.vue"
import StudentManagement from "@/components/AdminComp/StudentManagement.vue"
export default {
  name: 'AdminPage',
  data() {
    return {
      option:HanderComp.data().option
    }
  },
  methods: {
    getOption(option) {
      this.option = option
    }
  },
  components: {
    HanderComp,
    StudentManagement,
  }
}
</script>

<template>
  <div>
    <!-- 导航栏 -->
    <HanderComp  @update-option="getOption"></HanderComp>
    <!-- 学生管理 -->
    <StudentManagement v-if="option === 0" >学生管理</StudentManagement>
    <!-- 教师管理 -->
    <h1 v-if="option === 1">教师管理</h1>
    <!-- 学生宿舍外出管理 -->
    <h1 v-if="option === 2">学生宿舍外出管理</h1>
    <!-- 宿舍管理 -->
    <h1 v-if="option === 3">宿舍管理</h1>
  </div>
</template>

<style>
</style>