import {createRouter, createWebHistory} from 'vue-router/auto'
import {Router, RouteRecordRaw} from 'vue-router'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/welcome'
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  },
  {
    path: '/404',
    component: () => import('@/pages/NotFoundPage.vue'),
    meta: {title: 'TJLinker - Not Found'}
  },
  {
    path: '/home',
    component: () => import('@/pages/Home.vue'),
    meta: {title: 'TJLinker - Home'}
  },
  {
    path: '/chat',
    component: () => import('@/pages/Chat.vue'),
    meta: {title: 'TJLinker - Chat'}
  },
  {
    path: '/chat-personal',
    component: () => import('@/pages/ChatPersonal.vue'),
    meta: {title: 'TJLinker - Chat'}
  },
  {
    path: '/manage-team',
    component: () => import('@/pages/ManageTeam.vue'),
    meta: {title: 'TJLinker - Manage Team'}
  },
  {
    path: '/create-activity',
    component: () => import('@/pages/CreateActivity.vue'),
    meta: {title: 'TJLinker - CreateActivity'}
  },
  {
    path: '/detail-activity',
    component: () => import('@/pages/DetailActivity.vue'),
    meta: {title: 'TJLinker - DetailActivity'}
  },
  {
    path: '/detail-activity-manager',
    component: () => import('@/pages/DetailActivityManager.vue'),
    meta: {title: 'TJLinker - DetailActivityManager'}
  },
  {
    path: '/find-password',
    component: () => import('@/pages/FindPassword.vue'),
    meta: {title: 'TJLinker - FindPassword'}
  },
  {
    path: '/login',
    component: () => import('@/pages/Login.vue'),
    meta: {title: 'TJLinker - Login'}
  },
  {
    path: '/login/user',
    component: () => import('@/pages/LoginUser.vue'),
    meta: {title: 'TJLinker - Login'}
  },
  {
    path: '/login/manager',
    component: () => import('@/pages/LoginManager.vue'),
    meta: {title: 'TJLinker - Login'}
  },
  {
    path: '/manager',
    component: () => import('@/pages/Manager.vue'),
    meta: {title: 'TJLinker - Manager'}
  },

  {
    path: '/not-found-page',
    component: () => import('@/pages/NotFoundPage.vue'),
    meta: {title: 'TJLinker - NotFoundPage'}
  },
  {
    path: '/person',
    component: () => import('@/pages/Person.vue'),
    meta: {title: 'TJLinker - Person'}
  },

  {
    path: '/register',
    component: () => import('@/pages/Register.vue'),
    meta: {title: 'TJLinker - Register'}
  },
  {
    path: '/welcome',
    component: () => import('@/pages/Welcome.vue'),
    meta: {title: 'TJLinker - Welcome'}
  },
  
  {
    path: '/edituserinfo',
    component: () => import('@/pages/EditUserInfo.vue'),
    meta: {title: 'TJLinker - EditUserInfo'}
  },





  
]

const router: Router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, _, next) => {
  if (to.meta && to.meta.title) {
    document.title = to.meta.title as string
  } else {
    document.title = 'TJLinker'
  }
  next()
})

router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router



