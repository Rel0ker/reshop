import { ref, computed } from 'vue';
import { api } from '../api';

interface User {
  id: number;
  username: string;
  email: string;
  avatar?: string;
  role: string;
}

const user = ref<User | null>(null);
const token = ref<string | null>(localStorage.getItem('access_token'));
const isInitialized = ref(false);

export const isAuthenticated = computed(() => {
  console.log('[Auth] isAuthenticated computed:', !!token.value, 'Token:', token.value);
  return !!token.value;
});

// Установка токена и информации о пользователе
export function setAuth(newToken: string, userData: User) {
  console.log('[Auth] setAuth called with:', { token: newToken, user: userData });
  token.value = newToken;
  user.value = userData;
  localStorage.setItem('access_token', newToken);
}

// Очистка данных аутентификации
export function clearAuth() {
  console.log('[Auth] clearAuth called');
  token.value = null;
  user.value = null;
  localStorage.removeItem('access_token');
}

// Получение информации о пользователе
export async function fetchUser() {
  try {
    console.log('[Auth] fetchUser called, token:', token.value);
    if (!token.value) {
      console.log('[Auth] No token, skipping fetchUser');
      return;
    }
    
    const response = await api.get('/users/me/');
    console.log('[Auth] Профиль пользователя успешно загружен:', response.data);
    console.log('[Auth] Роль пользователя:', response.data.role);
    user.value = response.data;
  } catch (error) {
    console.error('[Auth] Ошибка при загрузке профиля:', error);
    clearAuth();
  }
}

// Вход в систему
export async function login(email: string, password: string) {
  try {
    console.log('[Auth] login called for:', email);
    const response = await api.post('/auth/login/', {
      email,
      password,
    });
    console.log('[Auth] Login response:', response.data);
    
    // Django возвращает access и refresh токены
    const accessToken = response.data.access;
    
    // Устанавливаем токен
    token.value = accessToken;
    localStorage.setItem('access_token', accessToken);
    
    // Получаем информацию о пользователе
    await fetchUser();
    return true;
  } catch (error) {
    console.error('Login error:', error);
    return false;
  }
}

// Регистрация
export async function register(username: string, email: string, password: string) {
  try {
    console.log('[Auth] register called for:', email);
    const response = await api.post('/auth/register/', {
      username,
      email,
      password,
    });
    console.log('[Auth] Register response:', response.data);
    setAuth(response.data.token, response.data.user);
    await fetchUser();
    return true;
  } catch (error) {
    console.error('Registration error:', error);
    return false;
  }
}

// Выход из системы
export function logout() {
  console.log('[Auth] logout called');
  clearAuth();
}

// Инициализация при загрузке приложения
export async function init() {
  console.log('[Auth] init called, token exists:', !!token.value);
  if (token.value) {
    console.log('[Auth] Token found, fetching user data');
    await fetchUser();
  } else {
    console.log('[Auth] No token found, user not authenticated');
  }
  isInitialized.value = true;
  console.log('[Auth] init completed, isAuthenticated:', isAuthenticated.value);
}

export function useAuth() {
  return {
    user,
    token,
    isAuthenticated,
    isInitialized,
    login,
    register,
    logout,
    init,
    setAuth,
    clearAuth,
    fetchUser,
  };
}