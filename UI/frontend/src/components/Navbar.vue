<template>
  <div>
      <nhs-header
        show-nav
        position="top"
        :service="{
          name: 'Data Lens',
          href: '/'
        }"
        :organisation="{
          name: 'Data Lens',
          split: 'Data Lens',
          descriptor: 'Data Lens',
          logoURL: 'https://i.ibb.co/cCGdt5d/nhsx-Data-Lens.png'
        }"> 
        
          <!-- <nhs-header-item href="/search/simple">Simple Search</nhs-header-item>
          <nhs-header-item href="/upload/file">Upload File</nhs-header-item>
          <nhs-header-item href="/logout">Logout</nhs-header-item> -->
      </nhs-header>
  </div>
</template>

<script>
  import {
      NhsHeader,
  } from 'nhsuk-frontend-vue';

  export default {
    name: "NavigationPage",
    components: {
      NhsHeader
    },
    methods: {
      navigateTo(type){
        this.$emit('navigate-to', type)

      }
    }
  };
  </script>

<style scoped>
  .nhsuk-org-logo {
    height: 40px;
  }

  .nhsuk-header {
    background-color: #003087;
  }
</style>
