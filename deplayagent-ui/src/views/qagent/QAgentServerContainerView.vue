<template>
  <div class="list-query-container">
    <!-- 上方：条件查询表单区域 -->
    <div class="search-form-wrapper">
      <el-form
        :model="searchForm"
        inline
        ref="searchFormRef"
        class="search-form"
        label-width="80px"
      >
        <el-form-item label="名称" prop="container_name">
          <el-input
            v-model="searchForm.container_name"
            placeholder="请输入名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="images_id" prop="images_id">
          <el-input
            v-model="searchForm.images_id"
            placeholder="请输入images_id"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="ports" prop="ports">
          <el-input
            v-model="searchForm.ports"
            placeholder="请输入ports"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>

        <el-form-item label="server_id" prop="server_id">
          <el-select
            v-model="searchForm.server_id"
            placeholder="请选择server_id"
            clearable
            style="width: 200px"
          >
            <el-option v-for="item in serverIds" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button @click="handleSyncData">同步容器信息</el-button>
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
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="server_id" label="服务器id" width="120" align="center">
          <template #default="scope">
            <template v-for="item in serverIds">
              <span  :key="item.id" v-if="scope.row.server_id === item.id">{{item.name}}</span>
            </template>
          </template>
        </el-table-column>
        <el-table-column prop="container_id" label="容器" align="center" />
        <el-table-column prop="container_name" label="容器名" width="150" align="center" />
        <el-table-column prop="work_path" label="工作空间" width="150" align="center" />
        <el-table-column prop="images_id" label="镜像" width="150" align="center" />
        <el-table-column prop="ports" label="ports" width="150" align="center" />
        <el-table-column prop="running_for" label="running_for" width="150" align="center" />
        <el-table-column prop="state" label="state" width="150" align="center" />
        <el-table-column prop="status" label="status" width="150" align="center" />
        <el-table-column prop="size" label="size" width="150" align="center" />
        <el-table-column prop="names" label="names" width="150" align="center" show-overflow-tooltip/>
        <el-table-column prop="labels" label="labels" width="150" align="center" show-overflow-tooltip/>
        <el-table-column label="操作" width="150" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleRestart(scope.row)">重启</el-button>
            <el-button type="danger" size="small" @click="handleDown(scope.row)">下架</el-button>
            <el-button type="info" size="small" @click="handleUp(scope.row)">上架</el-button>
            <el-button type="warning" size="small" @click="handleRollback(scope.row)">回滚</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

  </div>
</template>

<script setup>
import {ref, reactive, onMounted, watch} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {containerApi} from '@/api/qagent/container'
import {serverApi} from '@/api/qagent/server'
import {useRoute} from "vue-router";

const route = useRoute()

const refQuery = ref({})
const serverIds = ref([])
const refToken = ref(null)
// ============ 表单相关 ============
// 查询表单数据
const searchForm = reactive({
  server_id: null,
  container_name: null,
  images_id: null,
  ports: null,
})
// 表单ref，用于重置表单
const searchFormRef = ref(null)

// ============ 表格相关 ============
// 表格加载状态
const loading = ref(false)
// 表格数据源
const tableData = ref([])

onMounted(() => {
  getTableList()
})

/**
 * 获取表格列表数据（核心查询方法）
 */
const getTableList = async () => {
  try {
    loading.value = true
    // 1. 构造查询参数：合并【查询条件】和【分页条件】
    const params = {
      ...searchForm
    }
    const rows = await containerApi.list(params)
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
 * 点击重置按钮
 */
const handleReset = () => {
  // 重置表单所有数据为空
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = null
  })
  getTableList()
}


const handleSyncData = async (row)=>{
  try {
    await ElMessageBox.confirm('确定要同步容器数据吗？', '确认', {type: 'info'})
    await containerApi.syncdata(refToken.value)
    ElMessage.success('同步成功')
    getTableList()
  } catch {
    ElMessage.info('取消同步')
  }
}
const handleRestart = async (row)=>{
  try {
    await ElMessageBox.confirm('确定要重启容器吗？', '确认', {type: 'info'})
    await containerApi.restart(row.id)
    ElMessage.success('重启成功')
    getTableList()
  } catch {
    ElMessage.info('取消重启')
  }
}
const handleDown = async (row)=>{
  try {
    await ElMessageBox.confirm('确定要下架容器吗？', '确认', {type: 'info'})
    await containerApi.restart(row.id)
    ElMessage.success('下架成功')
    getTableList()
  } catch {
    ElMessage.info('取消下架')
  }
}
const handleUp = async (row)=>{
  try {
    await ElMessageBox.confirm('确定要上架容器吗？', '确认', {type: 'info'})
    await containerApi.restart(row.id)
    ElMessage.success('上架成功')
    getTableList()
  } catch {
    ElMessage.info('取消上架')
  }
}
const handleRollback = (row)=>{

}

const queryServerIds = async ()=>{
  try {
    const res = await serverApi.listids()
    serverIds.value = res || []
  } catch (_) {
    console.log(_)
  }
}


const queryToken = async ()=>{
  try {
    const res = await containerApi.token()
    refToken.value = res
  } catch (_) {
    console.log(_)
  }
}

watch(() => route.query, (newParams) => {
  console.log('参数变化了：', newParams)
  refQuery.value = {qagentId: newParams.qagentId}
  searchForm.server_id = refQuery.value.qagentId
  queryServerIds()
  queryToken()
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