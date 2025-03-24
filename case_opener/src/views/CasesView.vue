<template>
    <div class="cases">
        <!-- <CasesSite msg="tu sa skrzynki" /> -->
         <CasesSite />
    </div>
</template>

<script>
import CasesSite from '@/components/CasesSite.vue';
export default{
    name: "CasesView",
    components: {
        CasesSite
    }
}


</script>