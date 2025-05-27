<template>
    <div class="cases">
      <div v-if="isAuthenticated" class="container">
        <h1 class="title has-text-white">Witaj, {{ username }}!</h1>
        <div class="buttons is-flex is-justify-content-center">
          <div v-if="isOpening">
              <h1 class="title has-text-centered">Skrzynka sie otwiera...</h1>
          </div>
          <div v-else>
            <button @click="openCase(1)" class="button case-button">
            <img src="/assets/pobrane-_4_.png" alt="fracture_case" class="image is-128x128">
            <span class="case-name">Fracture Case</span>
          </button>
          <button @click="openCase(2)" class="button case-button">
            <img src="/assets/pobrane.png" alt="bravo_case" class="image is-128x128">
            <span class="case-name">Bravo Case</span>
          </button>
          </div>
        </div>
        <br>
        <!-- Animacja -->
        <div v-if="selected_image" class="case-animation-wrapper">
          <div class="gowno1">a</div>
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
          <p class="subtitle has-text-success">{{ lastDrop.skin_name }}</p>
          <p class="has-text-white">Rzadkość: </p><p class="has-text-link">{{ lastDrop.rarity }}</p>
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
        koniecAnim: false,
        isOpening: false,
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
            //4. ustawianie dropa
            const drop = {
            skin_name: response.data.skin_name,
            rarity: response.data.rarity,
            skin_src: response.data.skin_src
          };
          this.skinImages.push({ src: drop.skin_src });
          //5. inicjalizowanie animacji
          this.startAnimation(drop);
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
        startAnimation(drop) {
          this.isOpening = true;
          const itemWidth = 220;
          const visibleItems = 5;
          const targetIndex = this.skinImages.length - 1;
          const centerOffset = (itemWidth * visibleItems) / 2 - itemWidth / 2;
          const totalTranslate = targetIndex * itemWidth - centerOffset;

          let current = 0;
          const max = totalTranslate;
          const stepBase = 30;
          let slowdown = 0;

          this.rollInterval = setInterval(() => {
            const remaining = max - current;

            if (remaining < 1000) {
              slowdown += 0.3;
            }

            const step = Math.max(5, stepBase - slowdown);
            current += step;
            this.animationPosition = -current;

            if (current >= max) {
              clearInterval(this.rollInterval);
              this.rollInterval = null;

              // Możesz dodać dodatkowe skiny jeśli chcesz jeszcze przedłużyć taśmę
              for (let i = 0; i < 4; i++) {
                const randIndex = Math.floor(Math.random() * this.skinImages.length);
                this.skinImages.push({
                  src: this.skinImages[randIndex].src
                });
              }

              // Dopiero teraz pokazujemy dropa
              setTimeout(() => {
                this.lastDrop = drop;
                this.isOpening = false;
              }, 5000);

            }
          }, 16);
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
  border: 2px solid grey;
  width: 200px;
  height: auto;
  margin-right: 20px;
  flex-shrink: 0;
}

.gowno1{
    height: 100%;
    position: absolute;
    text-align: center;
    left: 50%;
    z-index: 1000;
    color: black;
    background-color: black;
    margin-left: auto;
    margin-right: auto;
}

  </style>
  