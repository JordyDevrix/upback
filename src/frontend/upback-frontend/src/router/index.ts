import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/tracked-apps',
        name: 'tracked-apps',
        component: () => import('../views/TrackedAppsView.vue')
    },
    {
        path: '/tracked-apps/:uuid',
        name: 'tracked-app-detail',
        component: () => import('../views/TrackedAppDetailView.vue'),
        props: true
    },
    {
        path: '/add-tracked-app',
        name: 'add-tracked-app',
        component: () => import('../views/AddTrackedAppView.vue'),
        props: true
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
