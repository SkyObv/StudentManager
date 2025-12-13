<script>
import ApplyHostelCard from "@/components/publicComp/ApplyHostelCard.vue";
export default {
  components: {
    ApplyHostelCard                               // 宿舍信息卡片
  },
  data() {
    return {
      hostelList: [{
            "id": 9,
            "hostel_number": "103",
            "floor": 1,
            "student_count": 0,
            "is_full": false,
            "gender": "female",
            "manager": "大大怪",
        }]
    }
  },
}
</script>

<template>
<div>
  <ApplyHostelCard v-for="item in hostelList" :key="item.id" :hostelInfo="item"></ApplyHostelCard>
</div>
</template>

<style scoped>

</style>