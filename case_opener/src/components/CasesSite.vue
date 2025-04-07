<template>
    <div class="cases">
        <div v-if="isAuthenticated" class="container">
            <h1 class="title has-text-white">Witaj, {{ username }}!</h1>
            <div class="buttons is-flex is-justify-content-center">
                <button @click="openCase(1)" class="button case-button">
                    <img src="../assets/pobrane-_4_.png" alt="fracture_case" class="image is-128x128">
                    <span class="case-name">Fracture Case</span>
                </button>
                <button @click="openCase(2)" class="button case-button">
                    <img src="../assets/pobrane.png" alt="bravo_case" class="image is-128x128">
                    <span class="case-name">Bravo Case</span>
                </button>
            </div>
            <br>
            <br>
            <div v-if="selected_image" class="content is-flex is-justify-content-center" >
                <div :class="{ move : doesMove}">
                    <h2>image</h2>
                <p><img :src="selected_image" alt="losowyDrop"></p>
                </div>
            </div>
            <!-- <h2>image</h2>
            <p v-if="selected_image" :class="{ move : doesMove}"><img :src="selected_image" alt="losowyDrop"></p> -->
            <div v-if="lastDrop" class="drop-result box has-background-dark">
                <h2 class="title has-text-white">Twój drop:</h2>
                <p class="subtitle has-text-white">{{ lastDrop.skin_name }}</p>
                <p class="has-text-white">Rzadkość: {{ lastDrop.rarity }}</p>
            </div>
        </div>
        
        <div v-else class="notification is-warning">
            Musisz się <router-link to="/log-in">zalogować</router-link>, aby otwierać skrzynki!
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import p250 from '@/assets/pobrane.png'
import redak from '@/assets/redak.png'
import p2500 from '@/assets/P250_See_Ya_Later.jpg'
import p25000 from '@/assets/P250_Przekl%3Fty_Apofis.jpg'


export default {
    name: "CasesSite",
    data() {
        return {
            isAuthenticated: false,
            username: '',
            lastDrop: null,
            token: localStorage.getItem('token') || null,
            images: [
                p250,
                redak,
                p2500,
                p25000
            ],
            selected_image: null,
            doesMove: false,
        }
    },
    async created() {
        await this.checkAuth();
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
        randomItem(items) {
                return items[Math.floor(Math.random() * items.length)];
        },
        async openCase(caseId) {
            if (!this.isAuthenticated) {
                alert('Musisz być zalogowany, aby otwierać skrzynki!');
                this.$router.push('/log-in');
                return;
            }

            try {
                const response = await axios.post(
                    `http://127.0.0.1:8000/api/v1/case/${caseId}/open/`, 
                    {},
                    {
                        headers: {
                            'Authorization': `Token ${this.token}`
                        }
                    }
                );
                this.lastDrop = {
                    skin_name: response.data.skin_name,
                    rarity: response.data.rarity
                };

                this.doesMove = true;
                let count = 0;
                const interval = setInterval(() => {
                    this.showDropAnimation();
                    console.log(count);
                    count++;

                    if(count >= 10){
                        clearInterval(interval);
                        console.log("end of the animation")
                    }
                }, 1000)
            } catch (error) {
                console.error('Error opening case:', error);
                alert('Wystąpił błąd podczas otwierania skrzynki');
            }
        },

        showDropAnimation() {
            this.selected_image = this.randomItem(this.images);
            this.doesMove = true;
            console.log('Playing drop animation...');
        }
    }
}
</script>

<style scoped>
.move {
    animation: move .4s alternate 30 ease-in-out;
}
@keyframes move {
    from {
        translate: 0 0;
    }
    to {
        translate: 70px 0;
    }
}
.case-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 20px;
}

.case-name {
    margin-top: 10px;
    color: white;
    font-weight: bold;
}

.drop-result {
    margin-top: 30px;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
    padding: 20px;
    border-radius: 10px;
}
</style>