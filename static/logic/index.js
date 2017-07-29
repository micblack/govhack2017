Vue.use('element-ui')
httpVueLoaderRegister(Vue, 'components/personas.vue');

let vm = new Vue({
	el: '#app',
	computed: {},
	data: {
		salutation: 'no change',
		sessionPersona: function () {
			return sessionStorage.getItem('persona') || ''
		}
	},
	methods: {
		personaChange(val) {
			sessionStorage.setItem('persona', val);
		}
	}
})