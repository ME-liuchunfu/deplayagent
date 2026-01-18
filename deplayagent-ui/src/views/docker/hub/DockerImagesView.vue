<template>
  <div class="list-query-container">
    <!-- 上方：条件查询表单区域 -->
    <div class="search-form-wrapper">
      <el-form
        inline
        ref="searchFormRef"
        class="search-form"
        label-width="80px"
      >
        <el-form-item label="hub" prop="hub">
          <el-select style="width: 200px" placeholder="请选择hubid" @change="handleHubChange">
            <el-option v-for="item in hubIds" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 下方：表格展示区域 -->
    <div class="table-wrapper">
      <el-table
        :data="tableData"
        border
        stripe
        v-loading="loading"
        element-loading-text="数据加载中..."
        fit
        highlight-current-row
        style="width: 100%"
      >
        <el-table-column prop="name" label="名称" width="120" align="center"/>
        <el-table-column prop="domain" label="domain" width="300" align="center" />
        <el-table-column prop="repo" label="repo" width="200" align="center" />
        <el-table-column label="tags" align="left">
          <template #default="scope">
            <div v-for="item in scope.row.tags" :key="item">{{item.size}} {{item.version}}
              <span style="color: #5ba0ff;cursor: pointer;" @click="commonUtil.copyTest(item.pull_url)"><el-icon><ElIconConnection /></el-icon></span>
              <span style="color: #ff4d4f;cursor: pointer;" @click="handleDel({repo: scope.row.repo, tag: item.version_code})"><el-icon><ElIconCloseBold /></el-icon></span>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import {ref, reactive, watch} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {imagesApi} from '@/api/docker/hub/images'
import {engineApi} from '@/api/docker/hub/engine'
import { useRoute } from 'vue-router'
import {commonUtil} from '@/utils/utils'

const route = useRoute()

const refQuery = ref({})
const hubIds = ref([])

const flushData = () =>{
   getTableList()
}

const handleHubChange = (val)=>{
  console.log(val)
  if (val) {
    refQuery.value.hubId = val
  }
}

const queryHubIds = async () =>{
    try{
      const rows = await engineApi.listids()
      hubIds.value = rows || []
    } catch (_) {
      console.error(_)
    }
}

// 表单ref，用于重置表单
const searchFormRef = ref(null)

// ============ 表格相关 ============
// 表格加载状态
const loading = ref(false)
// 表格数据源
const tableData = ref([])

/**
 * 获取表格列表数据（核心查询方法）
 */
const getTableList = async () => {
  try {
    if (!refQuery.value.hubId) {
      return
    }
    loading.value = true
    const rows = await imagesApi.list(refQuery.value.hubId)
    console.log('hub', rows)
    tableData.value = rows || []
  } catch (error) {
    ElMessage.error('数据查询失败，请稍后重试！')
    console.error('查询失败：', error)
  } finally {
    loading.value = false
  }
}

/**
 * 点击查询按钮
 */
const handleSearch = () => {
  getTableList()
}

/**
 * 删除行数据
 */
const handleDel = async (row) => {
  ElMessage.warning(`删除tag ID为【${row.tag}】数据`)
  try {
    await ElMessageBox.confirm('确定要删除这条数据吗？', '删除确认', {type: 'error'})
    await imagesApi.del({hub_id: refQuery.value.hubId, repo: row.repo, tag: row.tag})
    ElMessage.success('删除成功')
    getTableList()
  } catch {
    ElMessage.info('取消删除')
  }
}

watch(() => route.query, (newParams) => {
  console.log('参数变化了：', newParams)
  refQuery.value = {hubId: newParams.hubId}
  queryHubIds()
  flushData()
}, { immediate: true,deep: true })

</script>

<style scoped>
/* 整体容器 */
.list-query-container {
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}

/* 查询表单区域样式 */
.search-form-wrapper {
  background: #ffffff;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
}

/* 表格区域样式 */
.table-wrapper {
  background: #ffffff;
  padding: 20px;
  border-radius: 6px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.04);
}

/* 分页区域样式 */
.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}
</style>