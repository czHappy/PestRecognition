<template>
  <div class="container">
    <van-icon name="arrow-left" @click="back" class="back" />
    <div class="img">
      <img style="width:80%;height:80%;" :src="'data:image/png;base64,'+ img" alt="">
    </div>
    <div class="box">
      <van-button @click="fn" round block style="margin-top:30px;width:90%" color="linear-gradient(135deg,#56c8ff,#6f99fc) " type="primary">查看详情</van-button>
    </div>
    <van-popup closed="handdleClose" v-model="show" safe-area-inset-bottom position="bottom" :style="{ height: '60%' }">
      <div class="popup_box">
        <div class="little" v-for="(value, key, index) in getdetail" :key="index">
          <span></span>
          <div class="title">
            <span>Insect Code：{{value.INSECT_CODE}}</span>
            <span>Nums ：{{value.NUMS}}</span>
            <span>Order Name ：{{value.ORDER_NAME}}</span>
            <span>Familiy Name ：{{value.FAMILIY_NAME}}</span>
            <span>Genus Name：{{value.GENUS_NAME}}</span>
            <span>Insect Name：{{value.INSECT_NAME}}</span>
            <span>Latin Name：{{value.LATIN_NAME}}</span>
          </div>
        </div>

      </div>
    </van-popup>
  </div>
</template>

<script>
export default {
  data () {
    return {
      show: false
    }
  },
  created () {
  },
  computed: {
    img () {
      return this.$store.state.detail.img
    },
    getdetail () {
      const data = this.$store.state.detail
      delete data.img
      return data
    }
  },
  methods: {
    back () {
      this.$router.back()
    },
    fn () {
      this.show = true
    }
  }
}
</script>

<style lang="scss" scoped>
.back {
  font-size: 25px;
  margin-left: 20px;
  margin-top: 20px;
}
.box {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.container {
  width: 100%;
  height: 100%;
  background-image: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%);
  background-image: linear-gradient(to top, #fff1eb 0%, #ace0f9 100%);
  .img {
    width: 100%;
    display: flex;
    margin-top: 30px;
    justify-content: center;
    align-items: center;
  }
}
.popup_box {
  height: 100%;
  // width: 580px;
  display: flex;
  overflow-x: auto;
  white-space: nowrap;
  overflow: scroll;
  -overflow-scrolling: touch;
  box-sizing: border-box;
  background: linear-gradient(to top right, #d3959b, #bfe6ba);
}
.little {
  width: 280px;
  height: 100%;
  padding: 6px;
  padding-top: 0;
  padding-bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  .more {
    display: inline-block;
  }
  .title {
    padding-top: 10px;
    width: 240px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    // align-items: center;
    margin-left: 20px;
    word-wrap: break-word;
    word-break: break-all;
    span {
      font-size: 17px !important;
      margin-left: 5px;
      margin-right: 5px;
      white-space: pre-wrap;
      display: inline-block;
    }
    a {
      margin-left: 5px;
      font-weight: bold;
    }
  }
}
.little:last-child {
  margin-right: 0;
}
.popup_box::-webkit-scrollbar {
  display: none; /*隐藏滚动条*/
}
</style>
