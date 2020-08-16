import Vue from 'vue'
import Router from 'vue-router'
import App from '@/App'
import VueDemo from '@/components/VueDemo'
import StartPlatform from '@/components/StartPlatform'
import Messages from '@/components/Messages'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main',
      component: App
    },
    {
      path: '/demo',
      name: 'demo',
      component: VueDemo
    },
    {
      path: '/define',
      name: 'platform',
      component: StartPlatform
    },
    {
      path: '/messages',
      name: 'messages',
      component: Messages
    }
  ]
})
