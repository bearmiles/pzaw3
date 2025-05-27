<template>
    <div class="gowno">
        <Roulette ref="wheel" :items="items" @click="launchWheel"/>
    </div>
</template>
<script>
import { Roulette } from 'vue3-roulette';
export default{
    components: {
        Roulette,
    },
    data(){
        return {
            items : [
                {
                    id:1,
                    name: "1",
                    htmlContent: "1",
                    textColor: "",
                    background: "",
                },
                {
                    id: 2,
                    name: "2",
                    htmlContent: "2",
                    textColor: "",
                    background: "",
                },
                {
                    id: 3,
                    name: "3",
                    htmlContent: "3",
                    textColor: "",
                    background: "",
                },
                {
                    id: 4,
                    name: "4",
                    htmlContent: "4",
                    textColor: "",
                    background: "",
                },
                {
                    id: 5,
                    name: "5",
                    htmlContent: "5",
                    textColor: "",
                    background: "",
                },
                {
                    id: 6,
                    name: "6",
                    htmlContent: "6",
                    textColor: "",
                    background: "",
                },
            ],
        };
    },
    methods: {
        launchWheel(){
            this.$refs.wheel.launchWheel();
        }
    }
}
</script>
<style scoped>
.gowno{
    justify-content: center;
    text-align: center;
    margin-left: auto;
    margin-right: auto;
}
</style>