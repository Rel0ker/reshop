import { ref, computed } from 'vue';

// Состояние загрузки
const isLoading = ref(true);
const loadingProgress = ref(0);
const loadingText = ref('Инициализация приложения');
const loadingSteps = ref<string[]>([]);
const currentStep = ref(0);

// Вычисляемое свойство для определения, завершена ли загрузка
const isLoaded = computed(() => !isLoading.value);

// Функция для установки текста загрузки
const setLoadingText = (text: string) => {
  loadingText.value = text;
};

// Функция для установки прогресса
const setProgress = (progress: number) => {
  loadingProgress.value = Math.min(100, Math.max(0, progress));
};

// Функция для добавления шага загрузки
const addLoadingStep = (step: string) => {
  loadingSteps.value.push(step);
};

// Функция для перехода к следующему шагу
const nextStep = () => {
  if (currentStep.value < loadingSteps.value.length - 1) {
    currentStep.value++;
    setLoadingText(loadingSteps.value[currentStep.value]);
    setProgress((currentStep.value / (loadingSteps.value.length - 1)) * 100);
  }
};

// Функция для завершения загрузки
const finishLoading = () => {
  setProgress(100);
  setTimeout(() => {
    isLoading.value = false;
  }, 500); // Небольшая задержка для плавного перехода
};

// Функция для сброса состояния загрузки
const resetLoading = () => {
  isLoading.value = true;
  loadingProgress.value = 0;
  currentStep.value = 0;
  loadingSteps.value = [];
  loadingText.value = 'Инициализация приложения';
};

// Функция для имитации процесса загрузки
const simulateLoading = async (steps: string[], stepDelay: number = 800) => {
  resetLoading();
  loadingSteps.value = steps;
  
  for (let i = 0; i < steps.length; i++) {
    setLoadingText(steps[i]);
    setProgress((i / (steps.length - 1)) * 100);
    
    if (i < steps.length - 1) {
      await new Promise(resolve => setTimeout(resolve, stepDelay));
    }
  }
  
  finishLoading();
};

// Функция для быстрой загрузки
const quickLoad = async () => {
  const steps = [
    'Инициализация приложения',
    'Загрузка компонентов',
    'Подключение к API',
    'Готово!'
  ];
  
  await simulateLoading(steps, 300);
};

// Функция для детальной загрузки
const detailedLoad = async () => {
  const steps = [
    'Инициализация приложения',
    'Загрузка Vue компонентов',
    'Инициализация маршрутизатора',
    'Подключение к базе данных',
    'Загрузка пользовательских данных',
    'Инициализация состояния',
    'Готово!'
  ];
  
  await simulateLoading(steps, 1000);
};

export function useLoading() {
  return {
    // Состояние
    isLoading,
    loadingProgress,
    loadingText,
    loadingSteps,
    currentStep,
    isLoaded,
    
    // Методы
    setLoadingText,
    setProgress,
    addLoadingStep,
    nextStep,
    finishLoading,
    resetLoading,
    simulateLoading,
    quickLoad,
    detailedLoad
  };
}
