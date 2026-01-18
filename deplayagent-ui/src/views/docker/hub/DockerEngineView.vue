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
        <el-form-item label="名称" prop="name">
          <el-input
            v-model="searchForm.name"
            placeholder="请输入名称"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="domain" prop="domain">
          <el-input
            v-model="searchForm.domain"
            placeholder="请输入domain"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button @click="addFormShow = true">新增</el-button>
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
        <el-table-column prop="name" label="名称" width="120" align="center">
          <template #default="scope">
            <el-link style="color: #5ba0ff;" :underline="false"
                     @click="gotoImages(scope.row)"
                     >{{scope.row.name}}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="domain" label="domain" align="center" />
        <el-table-column prop="username" label="username" width="150" align="center" />
        <el-table-column prop="passwd" label="passwd" width="150" align="center" />
        <el-table-column label="操作" width="150" align="center">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDel(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增 -->
    <DockerEngineAddView
      :visible="addFormShow"
      :type="addFormType"
      :row-data="editRowData"
      @close="addFormShow = false"
      @success="getTableList"
    />
  </div>
</template>

<script setup>
import {ref, reactive, onMounted} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {engineApi} from '@/api/docker/hub/engine'
import router from "@/router";
import DockerEngineAddView from "@/views/docker/hub/DockerEngineAddView.vue";

// ============ 表单相关 ============
// 查询表单数据
const searchForm = reactive({
  name: null,
  domain: null
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

// ============ 核心方法 ============
const addFormShow = ref(false)
const addFormType = ref('add')
const editRowData = ref({})

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
    const rows = await engineApi.list(params)
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
 * 点击重置按钮
 */
const handleReset = () => {
  // 重置表单所有数据为空
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = null
  })
  getTableList()
}

const gotoImages = (row)=>{
  const p = {
    path:'/docker/hub/images',
    query: {
      hubId: row.id
    }
  }
  router.push(p)
}

/**
 * 编辑行数据
 */
const handleEdit = (row) => {
  ElMessage.info(`编辑ID为【${row.id}】的数据`)
  addFormType.value = 'edit'
  editRowData.value = row
  addFormShow.value = true
}

/**
 * 删除行数据
 */
const handleDel = async (row) => {
  ElMessage.warning(`删除ID为【${row.id}】数据`)
  try {
    await ElMessageBox.confirm('确定要删除这条数据吗？', '删除确认', { type: 'error' })
    await engineApi.del([row.id])
    ElMessage.success('删除成功')
    getTableList()
  } catch {
    ElMessage.info('取消删除')
  }
}
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