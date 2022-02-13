import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from "@/views/Index";
import Login from "@/views/Login";

Vue.use(VueRouter)


const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/',
        name: 'Index',
        component: Index,
        meta: {
            requiresAuth: true
        }
    }
]

const router = new VueRouter({
    mode: "history",
    routes
})

router.beforeEach((to, from, next) => {
    const isUserLoggedIn = localStorage.getItem('authenticated')
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (isUserLoggedIn) {
            next();
            return;
        }
        next('/login');
    }
    next();
});


export default router
