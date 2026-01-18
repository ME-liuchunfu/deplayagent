<template>
  <!-- 弹窗表单子组件：只负责弹窗和表单逻辑 -->
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="500px"
    destroy-on-close
    @closed="handleDialogClosed"
    append-to-body
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="100px"
      label-position="right"
    >
      <el-form-item label="服务名称" prop="name">
        <el-input
          v-model="formData.name"
          placeholder="请输入服务名称"
          clearable
          maxlength="50"
          show-word-limit
        />
      </el-form-item>
      <el-form-item label="服务域名/IP" prop="domain">
        <el-input
          v-model="formData.domain"
          placeholder="请输入服务域名或IP地址"
          clearable
          maxlength="128"
          show-word-limit
        />
      </el-form-item>
      <el-form-item label="登录账号" prop="username">
        <el-input
          v-model="formData.username"
          placeholder="请输入登录账号"
          clearable
          maxlength="128"
          show-word-limit
        />
      </el-form-item>
      <el-form-item label="登录密码" prop="passwd">
        <el-input
          v-model="formData.passwd"
          placeholder="请输入登录密码"
          clearable
          show-password
          maxlength="128"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleCancel">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          {{ isEdit ? '确认修改' : '确认新增' }}
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, watch, toRefs, defineEmits, defineProps } from 'vue'
import { ElMessage } from 'element-plus'
import {engineApi} from '@/api/docker/hub/engine'

const props = defineProps({
  // 弹窗是否显示
  visible: {
    type: Boolean,
    default: false
  },
  // 弹窗类型：add=新增 edit=编辑
  type: {
    type: String,
    default: 'add',
    validator: (val) => ['add', 'edit'].includes(val)
  },
  // 编辑时回显的表单数据，新增时为空对象
  rowData: {
    type: Object,
    default: () => ({})
  }
})
const { visible, type, rowData } = toRefs(props)

const emit = defineEmits(['close', 'success'])

// ============ 表单/弹窗相关数据 ============
const formRef = ref(null)
const dialogVisible = ref(visible.value)
const isEdit = ref(type.value === 'edit')
const dialogTitle = ref(isEdit.value ? '编辑服务' : '新增服务')
const submitLoading = ref(false)

// 表单数据 - 完美匹配DockerServer表结构
const formData = reactive({
  name: '',
  domain: '',
  username: '',
  passwd: ''
})

// 表单校验规则 - 和数据库字段约束一致
const formRules = reactive({
  name: [
    { required: true, message: '请输入服务名称', trigger: 'blur' },
    { min: 1, max: 50, message: '名称长度1-50字符', trigger: 'blur' }
  ],
  domain: [
    { required: true, message: '请输入域名/IP', trigger: 'blur' },
    { min: 1, max: 128, message: '域名长度1-128字符', trigger: 'blur' }
  ],
  username: [
    { required: true, message: '请输入登录账号', trigger: 'blur' },
    { min: 1, max: 128, message: '账号长度1-128字符', trigger: 'blur' }
  ],
  passwd: [
    { required: true, message: '请输入登录密码', trigger: 'blur' },
    { min: 1, max: 128, message: '密码长度1-128字符', trigger: 'blur' }
  ]
})

// 监听弹窗显示状态
watch(visible, (val) => {
  dialogVisible.value = val
  // 打开弹窗时，根据类型初始化表单
  if (val) {
    isEdit.value = type.value === 'edit'
    dialogTitle.value = isEdit.value ? '编辑服务' : '新增服务'
    initFormData()
  }
}, { immediate: true })

// 监听编辑数据变化，同步回显
watch(rowData, () => {
  if (isEdit.value) {
    initFormData()
  }
}, { deep: true })

// ============ 工具方法 ============
// 初始化表单数据：新增清空 / 编辑回显
const initFormData = () => {
  if (isEdit.value) {
    // 编辑：赋值回显数据，密码脱敏显示星号，保护隐私
    formData.name = rowData.value.name || ''
    formData.domain = rowData.value.domain || ''
    formData.username = rowData.value.username || ''
    formData.passwd = rowData.value.passwd || ''
  } else {
    // 新增：清空表单
    resetForm()
  }
}

// 重置表单+清除校验提示
const resetForm = () => {
  formData.name = ''
  formData.domain = ''
  formData.username = ''
  formData.passwd = ''
  formRef.value?.clearValidate()
}

// ============ 事件方法 ============
// 取消按钮 - 关闭弹窗
const handleCancel = () => {
  dialogVisible.value = false
  emit('close') // 向父组件抛关闭事件
}

// 弹窗关闭后重置表单
const handleDialogClosed = () => {
  resetForm()
  emit('close') // 向父组件抛关闭事件
}

const handleSubmit = async () => {
  // 1. 表单校验
  const valid = await formRef.value.validate()
  if (!valid) return

  try {
    submitLoading.value = true
    let res = {}
    // 新增请求
    if (!isEdit.value) {
      res = await engineApi.add(formData)
    } else {
      // 编辑请求 - 传主键id
      const editData = {...formData}
      editData['id'] = rowData.value.id
      res = await engineApi.put(editData)
    }
    console.log('hub', res)
    ElMessage.success(isEdit.value ? '编辑成功！' : '新增成功！')
    dialogVisible.value = false
    emit('success')
  } catch (error) {
    ElMessage.error('接口请求失败，请检查网络！')
    console.error('提交失败：', error)
  } finally {
    submitLoading.value = false
  }
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  width: 100%;
}
</style>