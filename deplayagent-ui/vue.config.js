const { defineConfig } = require('@vue/cli-service')
const {resolve} = require("path");
module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src') // 关键：@ 指向项目根目录下的 src 文件夹
      }
    }
  },
  // 开发环境下启用完整的源码映射
  chainWebpack: (config) => {
    if (process.env.NODE_ENV === 'development') {
      config.devtool('source-map')
    }
  }
})
