<template>
  <div id="app">
      <keep-alive>
        <router-view v-if="$route.meta.keepAlive"></router-view>
      </keep-alive>
      <router-view v-if="!$route.meta.keepAlive"></router-view>

  </div>
</template>

<script>
export default {
  data () {
    return {}
  },

  created () {
    // 在页面加载时读取sessionStorage里的状态信息
    if (sessionStorage.getItem('store')) {
      this.$store.replaceState(
        Object.assign(
          {},
          this.$store.state,
          JSON.parse(sessionStorage.getItem('store'))
        )
      )
    }
    // 在页面刷新时将vuex里的信息保存到sessionStorage里
    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem('store', JSON.stringify(this.$store.state))
    })
  }
}
</script>
<style lang="scss">
html,
body,
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}
.fade-enter-active,
.fade-leave-avtive {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
