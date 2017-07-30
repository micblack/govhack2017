Vue.use('element-ui')
httpVueLoaderRegister(Vue, 'static/components/personas.vue');
httpVueLoaderRegister(Vue, 'static/components/emergency.vue');

let vm = new Vue({
	el: '#app',
	computed: {},
	data: {
		prescriptions: [
			{
				title: 'Epilim',
				img: 'epilim.png',
				overdue: true,
				bulk: true,
				inStock: false
			},
			{
				title: 'CBD',
				img: 'cbd.png',
				overdue: false,
				bulk: false,
				inStock: true
			},
		]
	},
	methods: {}
})
