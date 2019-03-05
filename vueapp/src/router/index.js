
/* eslint-disable */

import Vue from 'vue'
import Router from 'vue-router'
import ActorList from '@/components/ActorList'
import ProductCreate from '@/components/ProductCreate'
import ActorDetail from '@/components/ActorDetail'
import Callback from '@/components/Callback'
import Home from '@/components/Home'
import Login from '@/components/Login'

Vue.use(Router)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path:'/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/actors',
    name: 'ActorList',
    component: ActorList,
  },
  {
    path: '/product-create',
    name: 'ProductCreate',
    component: ProductCreate,
    meta: { requiresAuth : true }    
  },
  {
    path: '/actors/:actor_name',
    name: 'ActorDetail',
    component: ActorDetail
  },
  {
    path: '/callback',
    name: 'Callback',
    component: Callback
  }]

const router = new Router({
  mode: 'history',
  routes
})

export default router
