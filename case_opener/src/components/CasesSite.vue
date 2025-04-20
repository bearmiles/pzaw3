<template>
    <div class="cases">
      <div v-if="isAuthenticated" class="container">
        <h1 class="title has-text-white">Witaj, {{ username }}!</h1>
        <div class="buttons is-flex is-justify-content-center">
          <button @click="openCase(1)" class="button case-button">
            <img src="/assets/pobrane-_4_.png" alt="fracture_case" class="image is-128x128">
            <span class="case-name">Fracture Case</span>
          </button>
          <button @click="openCase(2)" class="button case-button">
            <img src="/assets/pobrane.png" alt="bravo_case" class="image is-128x128">
            <span class="case-name">Bravo Case</span>
          </button>
        </div>
        <br>
        <!-- Animacja -->
        <div v-if="selected_image" class="case-animation-wrapper">
            <div
                class="case-animation-track"
                :style="{ transform: `translateX(${animationPosition}px)` }"
            >
                <img
                v-for="(skin, index) in skinImages"
                :key="index"
                :src="skin.src"
                alt="Skin"
                class="skin-item"
                />
            </div>
            </div>
        <!-- Wynik po zatrzymaniu animacji -->
        <div v-if="lastDrop" class="drop-result box has-background-dark">
          <h2 class="title has-text-white">Twój drop:</h2>
          <p class="subtitle has-text-white">{{ lastDrop.skin_name }}</p>
          <p class="has-text-white">Rzadkość: {{ lastDrop.rarity }}</p>
          <img :src="lastDrop.skin_src" alt="skin image" />
        </div>
      </div>
  
      <div v-else class="notification is-warning">
        Musisz się <router-link to="/log-in">zalogować</router-link>, aby otwierać skrzynki!
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: "CasesSite",
    data() {
      return {
        isAuthenticated: false,
        username: '',
        lastDrop: null,
        token: localStorage.getItem('token') || null,
        rollInterval: null,
        skinImages: [], // Array dla obrazków skinów
        selected_image: null, // Wylosowany obrazek
        animationPosition: -1000, // Początkowa pozycja animacji (poza ekranem)
        animationDuration: 5000, // Czas animacji w milisekundach
      };
    },
    async created() {
      await this.checkAuth();
    //   await this.loadSkinImages(caseId);
    },
    methods: {
      async checkAuth() {
        try {
          const response = await axios.get('http://127.0.0.1:8000/api/v1/user/', {
            headers: {
              'Authorization': `Token ${this.token}`
            }
          });
  
          this.isAuthenticated = true;
          this.username = response.data.username;
        } catch (error) {
          console.error('Auth check failed:', error);
          this.isAuthenticated = false;
          localStorage.removeItem('token');
  
          if (error.response?.status === 401 || error.response?.status === 404) {
            this.$router.push('/log-in');
          }
        }
      },
      async openCase(caseId) {
        if (!this.isAuthenticated) {
            alert('Musisz być zalogowany, aby otwierać skrzynki!');
            this.$router.push('/log-in');
            return;
        }

        try {
            // 1. Załaduj wszystkie skiny z tego case'a
            await this.loadSkinImages(caseId);

            this.selected_image = true
            // 2. Otwórz case i pobierz nagrodę
            const response = await axios.post(
            `http://127.0.0.1:8000/api/v1/case/${caseId}/open/`, 
            {},
            {
                headers: {
                'Authorization': `Token ${this.token}`
                }
            }
            );

            // 3. Ustaw dropa
            this.lastDrop = {
            skin_name: response.data.skin_name,
            rarity: response.data.rarity,
            skin_src: response.data.skin_src
            };

            // 4. Dodaj wylosowany skin jako ostatni obrazek na taśmie
            this.skinImages.push({ src: this.lastDrop.skin_src });

            // 5. Zainicjuj animację
            this.startAnimation();
        } catch (error) {
            console.error('Error opening case:', error);
            alert('Wystąpił błąd podczas otwierania skrzynki');
        }
        },
      async loadSkinImages(caseId) {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/cases/${caseId}/skins/`, {
            headers: {
                'Authorization': `Token ${this.token}`
            }
            });

            // Wypełniamy taśmę wieloma skinami (losowo z danych)
            const allSkins = response.data;
            const fakeRoll = [];

            // Dodaj losowe skiny (np. 30) na taśmę
            for (let i = 0; i < 30; i++) {
            const randIndex = Math.floor(Math.random() * allSkins.length);
            fakeRoll.push({
                src: allSkins[randIndex].skin_src
            });
            }

            this.skinImages = fakeRoll;
        } catch (error) {
            console.error('Error loading skins for animation:', error);
        }
        },
        startAnimation() {
            const itemWidth = 220; // szerokość skinów (img + margin)
            const visibleItems = 5; // ile skinów ma być widocznych
            const targetIndex = this.skinImages.length - 1; // ostatni element to nasz drop

            // Wylicz pozycję, by drop znalazł się idealnie na środku
            const centerOffset = (itemWidth * visibleItems) / 2 - itemWidth / 2;
            const totalTranslate = targetIndex * itemWidth - centerOffset;

            let current = 0;
            const max = totalTranslate;
            const stepBase = 30; // bazowa prędkość
            let slowdown = 0;

            this.rollInterval = setInterval(() => {
                const remaining = max - current;

                // Zwalnianie przy końcu
                if (remaining < 1000) {
                slowdown += 0.3;
                }

                const step = Math.max(5, stepBase - slowdown);

                current += step;
                this.animationPosition = -current;

                if (current >= max) {
                clearInterval(this.rollInterval);
                this.rollInterval = null;
                }
            }, 16); // ~60FPS
            }
    }
  }
  </script>
  
  <style scoped>
 .case-animation {
  width: 1100px;
  height: 200px;
  overflow: hidden;
  border: 2px solid #fff;
  position: relative;
  margin-top: 30px;
}

.case-animation::after {
  content: "";
  position: absolute;
  top: 0;
  left: 50%;
  width: 2px;
  height: 100%;
  background-color: red; /* znacznik środka */
  transform: translateX(-50%);
  z-index: 2;
}

.case-animation > div {
  display: flex;
  transition: none; /* animujemy JS-em */
}

.case-animation-wrapper {
  width: 100%;
  overflow: hidden;
  height: 200px;
  margin: 0 auto;
  border: 2px solid white;
  position: relative;
}

.case-animation-track {
  display: flex;
  transition: transform 5s ease-out;
  height: 100%;
}

.skin-item {
  width: 200px;
  height: auto;
  margin-right: 20px;
  flex-shrink: 0;
}

  </style>
  