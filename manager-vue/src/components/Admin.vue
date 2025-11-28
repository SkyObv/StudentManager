<script>
import HanderComp from "@/components/AdminComp/HanderComp.vue"
import FloorManage from "@/components/AdminComp/FloorManage.vue"
import HostelManage from "@/components/AdminComp/HostelManage.vue"
export default {
  name: 'AdminPage',
  data() {
    return {
      option:HanderComp.data().option,                               // 导航栏选项
      floorId: null,                                                 // 楼层ID
    }
  },
  methods: {
    // 导航栏点击
    getOption(option) {
      this.option = option
      this.floorId = null
    },
    // 楼层卡片点击详情页组件显示
    handleFloorClick(floorId) {
      this.floorId = floorId
      console.log('点击了楼层:', floorId);
      this.option = null
    },
    // 处理返回楼层管理页面
    handleGoBack() {
      this.floorId = null
      this.option = 0 // 重置为楼层管理页面的选项
    }
  },
  components: {
    HanderComp,
    FloorManage: FloorManage,
    HostelManage,
  }
}
</script>

<template>
  <div>
    <!-- 导航栏 -->
    <HanderComp  @update-option="getOption"></HanderComp>
    <!-- 宿舍管理 -->
    <FloorManage v-if="option === 0" @FloorClick="handleFloorClick"></FloorManage>
    <HostelManage v-if="floorId" @goBack="handleGoBack"></HostelManage>
    <!-- 教师管理 -->
    <h1 v-if="option === 1">教师管理</h1>
    <!-- 学生宿舍外出管理 -->
    <h1 v-if="option === 2">学生宿舍外出管理</h1>
    <!-- 学生管理 -->
    <h1 v-if="option === 3">宿舍管理</h1>
  </div>
</template>

<style>
</style>