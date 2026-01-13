<template>
   <div class="not-found-container">
      <!-- 背景装饰元素 -->
      <div class="bg-pattern"></div>

      <div class="content">
         <!-- 404数字动画 -->
         <div class="number-container">
            <span class="number" :style="{ '--i': 1 }">4</span>
            <div class="zero">
               <div class="eye left"></div>
               <div class="eye right"></div>
            </div>
            <span class="number" :style="{ '--i': 3 }">4</span>
         </div>

         <!-- 文本内容 -->
         <h1 class="title">页面不见了</h1>
         <p class="subtitle">
            抱歉，您访问的页面不存在或已被移除
         </p>

         <!-- 操作按钮 -->
         <div class="actions">
            <button
                class="btn primary"
                @click="$router.push('/')"
            >
               返回首页
            </button>
            <button
                class="btn secondary"
                @click="$router.go(-1)"
            >
               返回上一页
            </button>
         </div>
      </div>

      <!-- 底部装饰 -->
      <div class="footer">
         <p>Error code: 404</p>
      </div>
   </div>
</template>

<script setup>
// 可以在这里添加页面逻辑，如定时返回首页等功能
</script>

<style scoped>
.not-found-container {
   min-height: 100vh;
   display: flex;
   flex-direction: column;
   align-items: center;
   justify-content: center;
   background-color: #f8fafc;
   position: relative;
   overflow: hidden;
   padding: 2rem;
}

.bg-pattern {
   position: absolute;
   width: 100%;
   height: 100%;
   background-image:
       radial-gradient(rgba(148, 163, 184, 0.1) 1px, transparent 1px),
       radial-gradient(rgba(148, 163, 184, 0.1) 1px, transparent 1px);
   background-size: 50px 50px;
   background-position: 0 0, 25px 25px;
   z-index: 0;
}

.content {
   text-align: center;
   z-index: 1;
   max-width: 600px;
   width: 100%;
}

.number-container {
   display: flex;
   align-items: center;
   justify-content: center;
   gap: 1rem;
   margin-bottom: 2rem;
   perspective: 800px;
}

.number {
   font-size: clamp(8rem, 20vw, 15rem);
   font-weight: 900;
   color: #3b82f6;
   position: relative;
   animation: float 3s ease-in-out infinite;
   animation-delay: calc(var(--i) * 0.5s);
   text-shadow: 0 5px 15px rgba(59, 130, 246, 0.2);
}

.zero {
   width: clamp(8rem, 20vw, 15rem);
   height: clamp(8rem, 20vw, 15rem);
   border: 12px solid #3b82f6;
   border-radius: 50%;
   position: relative;
   animation: rotate 8s linear infinite;
   box-shadow: 0 5px 20px rgba(59, 130, 246, 0.2);
}

.eye {
   position: absolute;
   width: 20px;
   height: 20px;
   background-color: #3b82f6;
   border-radius: 50%;
   top: 35%;
   transition: all 0.3s ease;
}

.eye.left {
   left: 30%;
}

.eye.right {
   right: 30%;
}

/* 实现眼睛跟随鼠标移动效果 */
.not-found-container:hover .eye {
   width: 24px;
   height: 24px;
}

.title {
   font-size: clamp(2rem, 5vw, 3rem);
   font-weight: 700;
   color: #1e293b;
   margin-bottom: 1rem;
   animation: fadeInUp 0.8s ease forwards;
   opacity: 0;
}

.subtitle {
   font-size: clamp(1rem, 2vw, 1.25rem);
   color: #64748b;
   margin-bottom: 2.5rem;
   max-width: 400px;
   margin-left: auto;
   margin-right: auto;
   animation: fadeInUp 0.8s ease 0.2s forwards;
   opacity: 0;
}

.actions {
   display: flex;
   gap: 1rem;
   justify-content: center;
   flex-wrap: wrap;
   animation: fadeInUp 0.8s ease 0.4s forwards;
   opacity: 0;
}

.btn {
   padding: 0.875rem 2rem;
   border-radius: 8px;
   font-weight: 600;
   cursor: pointer;
   transition: all 0.3s ease;
   font-size: 1rem;
   border: none;
}

.btn.primary {
   background-color: #3b82f6;
   color: white;
}

.btn.primary:hover {
   background-color: #2563eb;
   transform: translateY(-2px);
   box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn.secondary {
   background-color: white;
   color: #3b82f6;
   border: 1px solid #dbeafe;
}

.btn.secondary:hover {
   background-color: #f1f5f9;
   transform: translateY(-2px);
}

.footer {
   position: absolute;
   bottom: 2rem;
   color: #94a3b8;
   font-size: 0.875rem;
   z-index: 1;
   animation: fadeIn 1.5s ease forwards;
}

/* 动画定义 */
@keyframes float {
   0%, 100% { transform: translateY(0) rotate(0deg); }
   50% { transform: translateY(-15px) rotate(2deg); }
}

@keyframes rotate {
   0% { transform: rotate(0deg); }
   100% { transform: rotate(360deg); }
}

@keyframes fadeInUp {
   from {
      opacity: 0;
      transform: translateY(20px);
   }
   to {
      opacity: 1;
      transform: translateY(0);
   }
}

@keyframes fadeIn {
   from { opacity: 0; }
   to { opacity: 1; }
}

/* 响应式调整 */
@media (max-width: 768px) {
   .number-container {
      gap: 0.5rem;
   }

   .btn {
      padding: 0.75rem 1.5rem;
      width: 100%;
   }
}
</style>
