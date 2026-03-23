<script>
import HanderComp from "@/components/AdminComp/HanderComp.vue"       // 导航栏
import FloorManage from "@/components/AdminComp/FloorManage.vue"     // 楼层管理
import HostelManage from "@/components/AdminComp/HostelManage.vue"   // 宿舍管理
import TeacherManage from "@/components/AdminComp/TeacherManage.vue" // 账号管理
import HostelLog from "@/components/AdminComp/HostelLog.vue";        // 宿舍申请审批
import CardIDManage from "@/components/AdminComp/CardIDManage.vue";  // 门禁管理
export default {
  name: 'AdminPage',
  data() {
    return {
      option:HanderComp.data().option,                               // 导航栏选项
      floorId: null,                                                 // 楼层ID点击
    }
  },
  methods: {
    // 导航栏点击
    getOption(option) {
      this.option = option
      this.floorId = null
      console.log(this.option)
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
    TeacherManage,
    HostelLog,
    CardIDManage
  }
}
</script>

<template>
  <div>
    <!-- 导航栏 -->
    <HanderComp  @update-option="getOption"></HanderComp>

    <!-- 宿舍管理 -->
    <FloorManage v-if="option === 0" @FloorClick="handleFloorClick"></FloorManage>
    <HostelManage v-if="floorId" @goBack="handleGoBack" :floorId="floorId"></HostelManage>

    <!-- 教师账号管理 -->
    <TeacherManage v-if="option === 1"></TeacherManage>

    <!-- 宿舍申请审批 -->
    <HostelLog v-if="option === 3"></HostelLog>

    <!-- 门禁卡管理 -->
    <CardIDManage v-if="option === 2"></CardIDManage>
  </div>
</template>

<style>
</style>