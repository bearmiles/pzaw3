import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CasesView from '@/views/CasesView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ProfileView from '@/views/ProfileView.vue'
import store from '@/store' // Importujesz store

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { requiresAuth: false }
  },
  {
    path: '/cases',
    name: 'cases',
    component: CasesView,
    meta: { requiresAuth: true } // Wymaga logowania
  },
  {
    path: '/log-in',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false, hideWhenAuthenticated: true } // Ukryj gdy zalogowany
  },
  {
    path: '/sign-up',
    name: 'signup',
    component: SignUpView,
    meta: { requiresAuth: false, hideWhenAuthenticated: true } // Ukryj gdy zalogowany
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true } // Wymaga logowania
  },
  {
    path: '/roulette',
    name: 'roulette',
    component: () => import('@/views/RouletteView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/log-in', '/sign-up'];
  const authRequired = !publicPages.includes(to.path);
  const token = localStorage.getItem('token');

  // Jeśli trasa wymaga autentykacji i nie ma tokenu
  if (authRequired && !token) {
    return next('/log-in');
  }

  // Jeśli użytkownik jest zalogowany i próbuje wejść na login/rejestrację
  if ((to.path === '/log-in' || to.path === '/sign-up') && token) {
    return next('/');
  }

  next();
});

export default router