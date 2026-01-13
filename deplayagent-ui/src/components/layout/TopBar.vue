<template>
  <div class="top-app-container">
    <div class="top-back" @click="handleBack">
      <ElIconArrowLeftBold />
    </div>
    <el-dropdown class="top-settings" placement="bottom-end">
      <div class="top-settings-btn"><ElIconMoreFilled /></div>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item v-for="(item, index) in settings" :key="index" @click="handleClick(item, index)">{{item.title}}</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
  </div>
</template>

<script setup>
import {defineProps, defineEmits} from "vue";

const props = defineProps({
  showBack: {
    type: Boolean,
    required: false,
    default: ()=> false
  },
  showSetting: {
    type: Boolean,
    required: false,
    default: ()=> false
  },
  settings: {
    type: Array,
    required: false,
    default: ()=> []
  }
})

const emits = defineEmits(["back", 'itemChoose'])

const handleClick = (item, index) => {
  emits('itemChoose', item, index)
}

const handleBack = ()=>{
  emits('back')
}
</script>

<style scoped>
.top-app-container {
  padding: 0 0.1rem;
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
  align-items: center;
  box-sizing: border-box;
  height: 0;
}
.top-back {
  width: 0.3rem;
  border-radius: 50%;
}
.top-settings, .top-settings-btn {
  width: 0.3rem;
}

.top-back, .top-settings {
  position: relative;
  margin-top: 0.4rem;
  padding: 0.05rem;
  /*background-color: rgba(255,255,255, 0.5);*/
  display: flex;
  justify-content: center;
  align-content: center;
  color: #2c3e50;
  cursor: pointer;
}
</style>
