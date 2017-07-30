Vue.use('element-ui')
httpVueLoaderRegister(Vue, 'components/personas.vue');
httpVueLoaderRegister(Vue, 'components/emergency.vue');

let vm = new Vue({
	el: '#app',
	computed: {},
	data: {
		wasWelcomed: sessionStorage.getItem('persona') || false,
		prescriptions: [
			'Cannabidoil',
			'Epilum 20mg'
		],
		selectedPrescriptions: []
	},	
	methods: {
		personaChange(val) {}
	}
})