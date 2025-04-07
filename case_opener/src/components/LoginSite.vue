<script>
    import axios from 'axios'

    export default{
        data() {
            return{
                form :{
                    fnm: '',
                    pwd: '',
                    nick: '',
                }
            };
        },
        methods: {
            async sendData() {
                try {
                    const response = await axios.post("http://127.0.0.1:8000/api/v1/loginn/", {
                    fnm: this.form.fnm,
                    pwd: this.form.pwd,
                    nick: this.form.nick,
                    });

                    console.log('Login successful:', response.data);
                    
                    // Zapisz token i dane użytkownika
                    localStorage.setItem('token', response.data.token);
                    localStorage.setItem('userNick', response.data.nick);
                    localStorage.setItem('userId', response.data.user_id);
                    
                    // Ustaw globalny stan
                    this.$root.isAuthenticated = true;
                    this.$root.username = response.data.nick;
                    
                    // Przekieruj na stronę główną
                    this.$router.push('/');
                    
                } catch (err) {
                    console.error("Login error:", err);
                    alert("Błąd logowania: " + (err.response?.data?.error || "Nieprawidłowe dane"));
                }
                }
    }
}


</script>

<template>
        <div class="hero is-fullheight is-black">
            <div class="hero-body">
            <div class="container has-text-centered">
            <div class="column is-8 is-offset-2">
                <h3 class="title has-text-white">Login</h3>
                <hr class="login-hr">
                <p class="subtitle has-text-white">Please login to see our cool stuff!</p>
<br>
<br>
<br>
                <form @submit.prevent="sendData">
                    <div class="field">
                        <div class="control">
                        <input v-model='form.nick' class="input is-large" type="text" placeholder="Nickname">
                        </div>
                    </div>
                    <br>
                    <div class="field">
                        <div class="control">
                        <input v-model="form.fnm" class="input is-large" type="email" placeholder="Email" autofocus="" required>
                        </div>
                    </div>
                    <br>
                    <div class="field">
                        <div class="control">
                        <input v-model='form.pwd' class="input is-large" type="password" placeholder="Password" required>
                        </div>
                    </div>
                    <br>
                <br>
                <br>
                <button type="submit" class="button is-block is-danger is-large is-fullwidth">Login</button>
                </form>
                <br>
                <br>
                <p class="subtitle has-text-white">Don't have an account? <RouterLink to="/sign-up">Register</RouterLink> </p>
            </div>
            </div>
        </div>
        </div>
</template>

