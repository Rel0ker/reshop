import { api } from '../api';

interface SampleProduct {
  title: string;
  description: string;
  price: number;
  quantity: number;
  usage_instructions: string;
}

const sampleProducts: SampleProduct[] = [
  {
    title: "Подписка ChatGPT Plus на 1 месяц",
    description: "Полный доступ к ChatGPT Plus с поддержкой GPT-4. Включает расширенные возможности, приоритетную поддержку и доступ к плагинам. MD5: a1b2c3d4e5f6g7h8i9j0",
    price: 2999,
    quantity: 50,
    usage_instructions: "После оплаты вы получите логин и пароль от аккаунта. Войдите на chat.openai.com и используйте все возможности Plus версии."
  },
  {
    title: "VPN Premium на 6 месяцев",
    description: "Высокоскоростной VPN с серверами в 50+ странах. Без логов, поддержка P2P, неограниченный трафик. MD5: b2c3d4e5f6g7h8i9j0k1",
    price: 1499,
    quantity: 100,
    usage_instructions: "Скачайте приложение, введите полученный ключ активации. Выберите сервер и наслаждайтесь безопасным интернетом."
  },
  {
    title: "Аккаунт Steam с играми",
    description: "Steam аккаунт с библиотекой из 25+ игр: GTA V, Cyberpunk 2077, Red Dead Redemption 2, и другие. MD5: c3d4e5f6g7h8i9j0k1l2",
    price: 8999,
    quantity: 10,
    usage_instructions: "Получите логин/пароль, смените пароль и email. Библиотека игр останется доступной."
  },
  {
    title: "Netflix Premium на 3 месяца",
    description: "Премиум подписка Netflix с 4K качеством, 4 экранами одновременно. Без рекламы, все сериалы и фильмы. MD5: d4e5f6g7h8i9j0k1l2m3",
    price: 1999,
    quantity: 75,
    usage_instructions: "Используйте полученные данные для входа в приложение Netflix. Подписка автоматически продлевается."
  },
  {
    title: "Spotify Premium на 1 год",
    description: "Годовая подписка Spotify Premium без рекламы, с возможностью скачивания музыки и высоким качеством звука. MD5: e5f6g7h8i9j0k1l2m3n4",
    price: 3999,
    quantity: 60,
    usage_instructions: "Активируйте подписку через полученную ссылку или код. Привяжите к своему аккаунту Spotify."
  },
  {
    title: "YouTube Premium на 6 месяцев",
    description: "Премиум доступ к YouTube без рекламы, фоновое воспроизведение, YouTube Music Premium. MD5: f6g7h8i9j0k1l2m3n4o5",
    price: 2499,
    quantity: 80,
    usage_instructions: "Войдите в аккаунт Google, активируйте Premium через полученный код. Наслаждайтесь YouTube без рекламы."
  },
  {
    title: "Discord Nitro на 1 месяц",
    description: "Премиум функции Discord: анимированные аватары, эмодзи, загрузка файлов до 100MB, HD стриминг. MD5: g7h8i9j0k1l2m3n4o5p6",
    price: 599,
    quantity: 120,
    usage_instructions: "Получите код активации, введите в настройках Discord. Nitro активируется мгновенно."
  },
  {
    title: "Twitch Turbo на 3 месяца",
    description: "Премиум подписка Twitch: без рекламы, эксклюзивные смайлики, поддержка стримеров. MD5: h8i9j0k1l2m3n4o5p6q7",
    price: 899,
    quantity: 90,
    usage_instructions: "Активируйте Turbo через полученный код в настройках Twitch. Наслаждайтесь стримами без рекламы."
  },
  {
    title: "Adobe Creative Cloud на 1 месяц",
    description: "Полный доступ к Adobe CC: Photoshop, Illustrator, Premiere Pro, After Effects и другие. MD5: i9j0k1l2m3n4o5p6q7r8",
    price: 5999,
    quantity: 25,
    usage_instructions: "Скачайте Adobe Creative Cloud, войдите с полученными данными. Все приложения будут доступны для установки."
  },
  {
    title: "Microsoft 365 на 1 год",
    description: "Годовая подписка Microsoft 365: Word, Excel, PowerPoint, Outlook, 1TB OneDrive. MD5: j0k1l2m3n4o5p6q7r8s9",
    price: 4999,
    quantity: 40,
    usage_instructions: "Активируйте подписку через Microsoft Account. Скачайте приложения Office и используйте облачное хранилище."
  },
  {
    title: "PlayStation Plus на 3 месяца",
    description: "Подписка PS Plus с ежемесячными играми, облачным сохранением, онлайн мультиплеером. MD5: k1l2m3n4o5p6q7r8s9t0",
    price: 1999,
    quantity: 70,
    usage_instructions: "Получите код активации, введите в PlayStation Store. Подписка активируется на вашем аккаунте."
  },
  {
    title: "Xbox Game Pass Ultimate на 1 месяц",
    description: "Ultimate подписка Xbox: сотни игр, Xbox Live Gold, EA Play, облачное гейминг. MD5: l2m3n4o5p6q7r8s9t0u1",
    price: 1499,
    quantity: 85,
    usage_instructions: "Активируйте код в Microsoft Store или на Xbox. Получите доступ к огромной библиотеке игр."
  },
  {
    title: "Nintendo Switch Online на 1 год",
    description: "Годовая подписка Nintendo Switch Online: онлайн мультиплеер, классические игры, облачные сохранения. MD5: m3n4o5p6q7r8s9t0u1v2",
    price: 1999,
    quantity: 55,
    usage_instructions: "Введите код в Nintendo eShop. Подписка активируется на вашем аккаунте Nintendo."
  },
  {
    title: "Origin Access Basic на 6 месяцев",
    description: "Полугодовой доступ к EA Play: более 60 игр, эксклюзивные скидки, ранний доступ к новинкам. MD5: n4o5p6q7r8s9t0u1v2w3",
    price: 1799,
    quantity: 65,
    usage_instructions: "Активируйте подписку через Origin или EA Desktop. Получите доступ к библиотеке игр EA."
  },
  {
    title: "Uplay+ на 3 месяца",
    description: "Квартальная подписка Ubisoft+: более 100 игр Ubisoft, включая новинки в день выхода. MD5: o5p6q7r8s9t0u1v2w3x4",
    price: 2499,
    quantity: 45,
    usage_instructions: "Войдите в Uplay с полученными данными. Все игры Ubisoft будут доступны для скачивания."
  },
  {
    title: "Epic Games Store ключи",
    description: "Набор из 10 популярных игр Epic Games Store: Borderlands 3, Metro Exodus, Control и другие. MD5: p6q7r8s9t0u1v2w3x4y5",
    price: 3999,
    quantity: 30,
    usage_instructions: "Получите ключи активации, введите их в Epic Games Store. Игры добавятся в вашу библиотеку."
  },
  {
    title: "GOG ключи игр",
    description: "Коллекция из 15 классических игр GOG: Witcher 3, Cyberpunk 2077, Divinity Original Sin 2. MD5: q7r8s9t0u1v2w3x4y5z6",
    price: 2999,
    quantity: 35,
    usage_instructions: "Активируйте ключи в GOG Galaxy или на сайте. Игры без DRM, скачивайте и играйте."
  },
  {
    title: "Humble Bundle ключи",
    description: "Набор из 20 игр из различных Humble Bundle: indie хитрости, AAA блокбастеры, классика. MD5: r8s9t0u1v2w3x4y5z6a7",
    price: 1999,
    quantity: 50,
    usage_instructions: "Получите ключи Steam, активируйте в своей библиотеке. Каждый ключ уникален и не использован."
  },
  {
    title: "Steam ключи популярных игр",
    description: "Коллекция из 25 топовых игр Steam: CS:GO, Dota 2, PUBG, Rust, ARK и другие. MD5: s9t0u1v2w3x4y5z6a7b8",
    price: 5999,
    quantity: 20,
    usage_instructions: "Активируйте ключи в Steam. Все игры лицензионные, добавятся в вашу библиотеку навсегда."
  },
  {
    title: "Minecraft Java Edition",
    description: "Полная версия Minecraft Java Edition с возможностью игры на серверах, модами, скинами. MD5: t0u1v2w3x4y5z6a7b8c9",
    price: 1999,
    quantity: 100,
    usage_instructions: "Получите логин/пароль от Mojang аккаунта. Скачайте игру с официального сайта Minecraft."
  },
  {
    title: "World of Warcraft подписка на 6 месяцев",
    description: "Полугодовая подписка WoW: доступ ко всем дополнениям, ежемесячные токены, привилегии подписчика. MD5: u1v2w3x4y5z6a7b8c9d0",
    price: 3999,
    quantity: 40,
    usage_instructions: "Активируйте подписку через Battle.net. Получите доступ ко всем мирам и контенту WoW."
  },
  {
    title: "Final Fantasy XIV подписка на 3 месяца",
    description: "Квартальная подписка FFXIV: полный доступ к игре, все дополнения, ежемесячные награды. MD5: v2w3x4y5z6a7b8c9d0e1",
    price: 2999,
    quantity: 55,
    usage_instructions: "Введите код активации в Mog Station. Подписка продлит ваш аккаунт на 90 дней."
  },
  {
    title: "EVE Online подписка на 1 год",
    description: "Годовая подписка EVE Online: Omega статус, все возможности игры, эксклюзивные корабли. MD5: w3x4y5z6a7b8c9d0e1f2",
    price: 7999,
    quantity: 25,
    usage_instructions: "Активируйте подписку через EVE Account Management. Получите Omega статус на 12 месяцев."
  },
  {
    title: "League of Legends RP карты",
    description: "Набор из 5 карт по 1350 RP для League of Legends. Покупайте чемпионов, скины, бусты. MD5: x4y5z6a7b8c9d0e1f2g3",
    price: 999,
    quantity: 200,
    usage_instructions: "Получите коды карт, введите их в League of Legends. RP зачислятся на ваш аккаунт."
  },
  {
    title: "Dota 2 Plus подписка на 1 месяц",
    description: "Месячная подписка Dota 2 Plus: статистика матчей, геройские роли, эксклюзивные сеты. MD5: y5z6a7b8c9d0e1f2g3h4",
    price: 799,
    quantity: 150,
    usage_instructions: "Активируйте подписку в игре Dota 2. Получите доступ ко всем функциям Plus."
  },
  {
    title: "Overwatch 2 боевой пропуск",
    description: "Боевой пропуск Overwatch 2: эксклюзивные скины, эмоции, позы, спреи, викторины. MD5: z6a7b8c9d0e1f2g3h4i5",
    price: 1499,
    quantity: 80,
    usage_instructions: "Получите код активации, введите в Overwatch 2. Боевой пропуск активируется на вашем аккаунте."
  },
  {
    title: "Valorant боевой пропусс",
    description: "Боевой пропусс Valorant: эксклюзивные скины оружия, карточки игроков, эмоции, спреи. MD5: a7b8c9d0e1f2g3h4i5j6",
    price: 1299,
    quantity: 95,
    usage_instructions: "Активируйте код в игре Valorant. Получите доступ ко всем наградам боевого пропуска."
  },
  {
    title: "CS:GO Prime Status",
    description: "Prime статус CS:GO: приоритетные матчи, эксклюзивные награды, защита от читеров. MD5: b8c9d0e1f2g3h4i5j6k7",
    price: 999,
    quantity: 120,
    usage_instructions: "Получите код активации, введите в Steam. Prime статус активируется на вашем аккаунте."
  },
  {
    title: "PUBG: BATTLEGROUNDS Plus",
    description: "Plus подписка PUBG: эксклюзивные награды, ежемесячные скины, приоритетная поддержка. MD5: c9d0e1f2g3h4i5j6k7l8",
    price: 899,
    quantity: 110,
    usage_instructions: "Активируйте подписку в игре PUBG. Получите доступ ко всем Plus функциям."
  },
  {
    title: "Fortnite Crew подписка на 1 месяц",
    description: "Месячная подписка Fortnite Crew: эксклюзивный скин, 1000 V-Bucks, боевой пропусс. MD5: d0e1f2g3h4i5j6k7l8m9",
    price: 999,
    quantity: 130,
    usage_instructions: "Получите код активации, введите в Epic Games. Подписка Crew активируется на месяц."
  },
  {
    title: "Apex Legends боевой пропусс",
    description: "Боевой пропусс Apex Legends: эксклюзивные скины, эмоции, финшеры, голосовые линии. MD5: e1f2g3h4i5j6k7l8m9n0",
    price: 1199,
    quantity: 85,
    usage_instructions: "Активируйте код в игре Apex Legends. Получите доступ ко всем наградам сезона."
  },
  {
    title: "Rainbow Six Siege Year Pass",
    description: "Годовой пропуск Rainbow Six Siege: все операторы года, эксклюзивные скины, бонусы. MD5: f2g3h4i5j6k7l8m9n0o1",
    price: 3999,
    quantity: 45,
    usage_instructions: "Получите код активации, введите в Uplay. Годовой пропусс активируется на вашем аккаунте."
  },
  {
    title: "Destiny 2 сезонный пропусс",
    description: "Сезонный пропусс Destiny 2: эксклюзивные награды, сюжетные миссии, оружие, доспехи. MD5: g3h4i5j6k7l8m9n0o1p2",
    price: 1499,
    quantity: 70,
    usage_instructions: "Активируйте код в игре Destiny 2. Получите доступ ко всему контенту сезона."
  },
  {
    title: "GTA Online Shark Cards",
    description: "Набор из 3 Shark Cards GTA Online: $1,250,000, $2,000,000, $3,500,000 для покупки всего. MD5: h4i5j6k7l8m9n0o1p2q3",
    price: 2999,
    quantity: 60,
    usage_instructions: "Получите коды карт, введите их в GTA Online. Деньги зачислятся на ваш аккаунт."
  },
  {
    title: "Red Dead Online Gold Bars",
    description: "Пакет из 50 Gold Bars для Red Dead Online: покупка оружия, лошадей, одежды, улучшений. MD5: i5j6k7l8m9n0o1p2q3r4",
    price: 1999,
    quantity: 75,
    usage_instructions: "Активируйте код в Red Dead Online. Gold Bars появятся в вашем инвентаре."
  },
  {
    title: "FIFA 23 Ultimate Team Coins",
    description: "1,000,000 монет FIFA 23 Ultimate Team для покупки игроков, улучшения команды, открытия паков. MD5: j6k7l8m9n0o1p2q3r4s5",
    price: 3999,
    quantity: 40,
    usage_instructions: "Получите код активации, введите в FIFA 23. Монеты зачислятся на ваш Ultimate Team."
  },
  {
    title: "Call of Duty: Warzone CoD Points",
    description: "2400 CoD Points для Call of Duty: Warzone: покупка боевых пропуссов, скинов, бандлов. MD5: k7l8m9n0o1p2q3r4s5t6",
    price: 1799,
    quantity: 90,
    usage_instructions: "Активируйте код в Call of Duty. CoD Points появятся на вашем аккаунте."
  }
];

export async function addSampleProducts(progressCallback?: (current: number) => void) {
  console.log('Начинаю добавление образцов товаров...');
  
  // Небольшая задержка в начале для лучшего UX
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  for (let i = 0; i < sampleProducts.length; i++) {
    const product = sampleProducts[i];
    
    try {
      console.log(`Добавляю товар ${i + 1}/${sampleProducts.length}: ${product.title}`);
      
      // Обновляем прогресс
      if (progressCallback) {
        progressCallback(i + 1);
      }
      
      const formData = new FormData();
      formData.append('title', product.title);
      formData.append('description', product.description);
      formData.append('price', String(product.price));
      formData.append('quantity', String(product.quantity));
      formData.append('usage_instructions', product.usage_instructions);
      
      // Добавляем информацию о продавце
      formData.append('seller_info', 'seller@gmail.com - Надежный продавец цифровых товаров');
      
      // Добавляем пустое изображение (можно заменить на реальное)
      const emptyBlob = new Blob([''], { type: 'image/png' });
      const emptyFile = new File([emptyBlob], 'placeholder.png', { type: 'image/png' });
      formData.append('uploaded_images', emptyFile);
      
      const response = await api.post('/products/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      console.log(`✅ Товар "${product.title}" успешно добавлен!`);
      
      // Небольшая задержка между запросами
      await new Promise(resolve => setTimeout(resolve, 500));
      
    } catch (error: any) {
      console.error(`❌ Ошибка при добавлении товара "${product.title}":`, error);
      
      if (error.response?.data) {
        console.error('Детали ошибки:', error.response.data);
      }
    }
  }
  
  console.log('🎉 Добавление образцов товаров завершено!');
}

export { sampleProducts };
