import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    detail: {},
    imgobj: {}
  },
  mutations: {
    DETAIL (state, data1) {
      state.detail = data1
    },
    IMG (state, data) {
      console.log(data)
      state.imgobj.aa = data
    }
  },
  actions: {
  },
  modules: {
  }
})
