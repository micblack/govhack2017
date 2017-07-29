Vue.use('element-ui')
httpVueLoaderRegister(Vue, 'components/personas.vue');

let vm = new Vue({
	el: '#app',
	computed: {},
	data: {
		salutation: 'no change'
	},
	methods: {
		personaChange(val) {}
	}
})