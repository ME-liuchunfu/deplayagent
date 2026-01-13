<template>
  <div
      v-show="show"
      class="context-menu"
      :style="{ top: contextMenuTop + 'px', left: contextMenuLeft + 'px' }"
  >
    <div v-for="(item, index) in itemList" :key="index+''"
         class="menu-item"
         v-show="item.show"
         @click="handleClick(item, index)">{{item.title}}</div>
  </div>
</template>

<script setup>
import {defineProps, defineEmits} from "vue";

const props = defineProps({
  show: {
    type: Boolean,
    required: false
  },
  contextMenuTop: {
    type: Number,
    required: false,
    default: ()=> 0
  },
  contextMenuLeft: {
    type: Number,
    required: false,
    default: ()=> 0
  },
  itemList: {
    type: Array,
    required: false,
    default: ()=>[]
  }
})

const emits = defineEmits(['itemChoose'])

const handleClick = (item, index) => {
    emits('itemChoose', item, index)
}

</script>

<style scoped>

.context-menu {
  position: fixed;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  z-index: 999;
  padding: 5px 0;
}

.menu-item {
  padding: 8px 20px;
  cursor: pointer;
  font-size: 14px;
}

.menu-item:hover {
  background: #f5f7fa;
}
.cursor{
  cursor: pointer;
}
</style>
