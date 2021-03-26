<template>
  <div>
      <div id="google_translate_element"></div>
  </div>
</template>

<script>
  export default {
    name: "Translation",
    data(){
        return{
            language : 'es'
        }
    },
    components: {
    },
    methods: {
    },
    mounted() {
        let externalScript = document.createElement('script')
        externalScript.setAttribute('src', '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit')
        document.body.appendChild(externalScript)

        this.$nextTick(function () {
            let func = document.createElement('script')
            func.innerHTML = "function googleTranslateElementInit() { new google.translate.TranslateElement({pageLanguage: 'en', includedLanguages: 'es', autoDisplay: false}, 'google_translate_element'); var a = document.querySelector(\"#google_translate_element select\"); console.log(a); a.selectedIndex=1; var event; if(typeof(Event) === 'function') {event = new Event('change');}else{event = document.createEvent('Event');event.initEvent('change');}a.dispatchEvent(event); }"
            document.body.appendChild(func);
        })
    },
  };
  </script>

<style>
    #google_translate_element,.skiptranslate{
        display:none;
    }

    body{
        top:0!important;
    }
</style>
