<template>
  <transition name="fade" mode="out-in">
    <div class="container">
      <div class="main" v-show="isshow">
        <span class="time">{{str}}</span>
        <div class="pic">
          <img src="../assets/logo.png" alt="">
          <div>
            <span class="title">林业有害生物识别系统</span>
            <span class="zuo">sk49</span>
          </div>
        </div>
      </div>

      <div class="box">
        <van-uploader preview-size="150px" :after-read="onRead" v-model="fileList" :max-count="1" @delete="handd"  />
        <br />
        <van-button style="width:90%;padding:20px;" block round :loading='isloading' loading-text="识别中..." color="linear-gradient(135deg,#56c8ff,#6f99fc) " @click="fn(1)" class="upload" icon="plus" type="primary" >识别害虫</van-button>
        <br />
        <van-button style="width:90%;padding:20px;" block round class="upload2" type="primary" color="linear-gradient(135deg,#56c8ff,#6f99fc) " icon="search" @click="fn(2)" :loading='isloading2' loading-text="识别中..." >检测害⾍</van-button>
      </div>

      <van-popover v-model="showPopover" placement="top-start" style="z-index=99999999" closed="handdleClose" trigger="click" :actions="actions">
        <div class="order">
          <span>Order Code：{{propMsg.ORDER_CODE}}</span>
          <span>Familiy Code：{{propMsg.FAMILIY_CODE }}</span>
          <span>Genus Code：{{propMsg.GENUS_CODE }}</span>
          <span>Insect code：{{propMsg.INSECT_CODE}}</span>
          <span>Food：{{propMsg.FOOD}}</span>
          <span>Area：{{propMsg.AREA}}</span>
        </div>
      </van-popover>
      <van-popup closed="handdleClose" v-model="show" safe-area-inset-bottom position="bottom" :style="{ height: '65%' }">
        <div class="popup_box">
          <div class="little">
            <van-image round cover width="180" height="180" :src="'data:image/png;base64,'+this.imgList1" @click="Image('data:image/png;base64,'+imgList1)" />
            <div class="title">
              <span>置信度:{{this.score1 + '%'}}</span>
              <span>Order Name：{{class1.ORDER_NAME}}</span>
              <span>Familiy Name：{{class1.FAMILIY_NAME}}</span>
              <span>Genus Name：{{class1.GENUS_NAME}}</span>
              <span>Insect Name：{{class1.INSECT_NAME}}</span>
              <span>Lattn Name：{{class1.LATIN_NAME}}</span>
              <div class="more">
                <a href="#" @click="more('class1')">查看更多...
                </a>
              </div>
            </div>

          </div>
          <div class="little">
            <van-image round contain @click="Image(e)" fit="cover" width="180" height="180" :src="'data:image/png;base64,'+this.imgList2" />
            <div class="title">
              <span>置信度:{{this.score2 + '%'}}</span>
              <span>Order Name：{{class2.ORDER_NAME}}</span>
              <span>Familiy Name：{{class2.FAMILIY_NAME}}</span>
              <span>Genus Name：{{class2.GENUS_NAME}}</span>
              <span>Insect Name：{{class2.INSECT_NAME}}</span>
              <span>Lattn Name：{{class2.LATIN_NAME}}</span>
              <a href="#" @click="more('class2')">查看更多...</a>
            </div>

          </div>
          <div class="little">
            <van-image round contain fit="cover" width="180" height="180" :src="'data:image/png;base64,'+this.imgList3" />
            <div class="title">
              <span>置信度:{{this.score3 + '%'}}</span>
              <span>Order Name：{{class3.ORDER_NAME}}</span>
              <span>Familiy Name：{{class3.FAMILIY_NAME}}</span>
              <span>Genus Name：{{class3.GENUS_NAME}}</span>
              <span>Insect Name：{{class3.INSECT_NAME}}</span>
              <span>Lattn Name：{{class3.LATIN_NAME}}</span>
              <a href="#" @click="more('class3')">查看更多...</a>
            </div>
          </div>
        </div>
      </van-popup>
    </div>
  </transition>

</template>

<script>
import Vue from 'vue'
import { ImagePreview, Toast } from 'vant'

Vue.use(ImagePreview, Toast)

export default {
  data () {
    return {
      str: 3,
      isshow: true,
      showPopover: false,
      actions: [],
      isloading: false,
      isloading2: false,
      show: false,
      file: {},
      fileList: [],
      imgList1: '',
      imgList2: '',
      imgList3: '',
      score1: '',
      score2: '',
      score3: '',
      class1: {},
      class2: {},
      class3: {},
      propMsg: {}
    }
  },
  // activated是页面激活后的钩子函数，一进页面就会触发
  activated () {
    // 显示时
    console.log(1)
  },
  created () {
    this.isshow = true
    const that = this
    const timer = setInterval(() => {
      that.str--
      if (that.str === 1) {
        setTimeout(() => {
          that.isshow = false
        }, 1000)
        clearInterval(timer)
      }
    }, 1000)
  },
  methods: {
    handd (file) {
      this.file = ''
    },
    detection () {
      // this.$axios.get('')
    },
    // 关闭 弹出层
    handdleClose () {
      this.class1 = {}
      this.class2 = {}
      this.class3 = {}
      this.score1 = ''
      this.score2 = ''
      this.score3 = ''
      this.imgList1 = ''
      this.imgList2 = ''
      this.imgList3 = ''
      this.propMsg = {}
    },
    // 查看更多
    more (val) {
      switch (val) {
        case 'class1':
          // eslint-disable-next-line no-case-declarations
          const obj = this.class1
          for (const key in obj) {
            this.$set(this.propMsg, key, obj[key])
          }
          break
        case 'class2':
          // eslint-disable-next-line no-case-declarations
          const obj2 = this.class2
          for (const key in obj2) {
            this.$set(this.propMsg, key, obj2[key])
          }
          break
        case 'class3':
          // eslint-disable-next-line no-case-declarations
          const obj3 = this.class3
          for (const key in obj3) {
            this.$set(this.propMsg, key, obj3[key])
          }
          break
      }
      this.showPopover = true
    },
    // 第一个按钮
    fn (v) {
      if (Object.keys(this.file).length === 0) {
        alert('请选择文件')
        return false
      }
      var formData = new FormData()
      formData.append('file', this.file.file) // 接口需要传的参数
      if (v === 1) {
        this.isloading = true
        this.$axios
          .post('http://10.1.69.33:5002/predict?', formData)
          .then((res) => {
            console.log(res)
            if (Object.keys(res.data).length === 0) {
              alert('接口返回空')
              this.isloading = false
              return
            }
            const {
              img1,
              img2,
              img3,
              score1,
              score2,
              score3,
              class1,
              class2,
              class3
            } = res.data
            this.score1 = score1
            this.score2 = score2
            this.score3 = score3
            this.imgList1 = img1
            this.imgList2 = img2
            this.imgList3 = img3
            this.class1 = class1
            this.class2 = class2
            this.class3 = class3
            this.show = true
            this.isloading = false
          })
      } else if (v === 2) {
        this.isloading2 = true
        this.$axios
          .post('http://10.1.69.33:5002/detect?', formData)
          .then((res) => {
            if (res.status === 200 && res.data.img) {
              this.$store.commit('DETAIL', res.data)
              const toast = Toast.loading({
                duration: 0, // 持续展示 toast
                forbidClick: true,
                message: '正在跳转结果页面'
              })

              let second = 1
              const timer = setInterval(() => {
                second--
                if (second) {
                  toast.message = '正在跳转结果页面'
                } else {
                  this.$router.push({
                    path: '/detail'
                  })
                  clearInterval(timer)
                  // 手动清除 Toast
                  Toast.clear()
                }
              }, 300)
              this.isloading2 = false
            }
          })
          .catch((error) => {
            alert('出错了')
            console.log(error)
          })
      }
    },
    onRead (file) {
      console.log(file)
      this.file = file
    }
  }
}
</script>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-avtive {
  transition: opacity 0.3s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.main {
  width: 100vw;
  height: 100vh;
  background: white;
  box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.16);
  .time {
    float: right;
    margin-right: 20px;
    margin-top: 20px;
    font-size: 20px;
    font-weight: bold;
    color: #80867f;
  }
  .pic {
    position: fixed;
    bottom: 20px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    img {
      width: 100px;
      height: 100px;
      margin-right: 10px;
      position: relative;
      left: 10px;
    }
    div {
      width: 50%;
      height: 55px;
      display: flex;
      flex-direction: column;
      // align-items: center;
      justify-content: space-around;
    }
    .title {
      color: #80867f;
      font-weight: 550;
      font-family: PingFangSC-Regular, PingFang SC;
    }
    .zuo {
      color: #b1b8b3;
    }
  }
}
.box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 35px;
}
.container {
  background-image: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%);
  background-image: linear-gradient(to top, #fff1eb 0%, #ace0f9 100%);
  height: 100%;
  width: 100%;
  background-size: 100% 100%;
  position: fixed; //固定定位
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
}
.little {
  background: linear-gradient(91deg, #f1eefc, #9dc6ff 70%, #a5bcff);
  width: 280px;
  height: 100%;
  padding: 6px;
  padding-top: 0;
  padding-bottom: 0;
  margin-right: 70px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-top-right-radius: 40px;
  border-top-left-radius: 40px;
  .more {
    display: inline-block;
  }
  .title {
    width: 240px;
    height: calc(100% - 160px);
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    // align-items: center;
    margin-left: 20px;
    word-wrap: break-word;
    word-break: break-all;
    span {
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

  .img {
    margin-top: 5px;
    width: 180px;
    height: 160px;
    border-radius: 50%;
  }
}
.little:last-child {
  margin-right: 0;
}
.popup_box::-webkit-scrollbar {
  display: none; /*隐藏滚动条*/
}
.order {
  position: relative;
  padding: 5px;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  word-break: break-all;
  cursor: text;
}
.van-popover[data-popper-placement="top-start"] .van-popover__arrow {
  display: none !important;
}
.order {
  padding-top: 10px !important;
}
</style>
