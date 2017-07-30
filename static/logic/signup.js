Vue.use('element-ui')
httpVueLoaderRegister(Vue, 'static/components/personas.vue');

let vm = new Vue({
	delimiters: ['{[{', '}]}'],
	el: '#app',
	computed: {},
	data: {
		newUser: {
			firstName: '',
			lastName: '',
			email: '',
			persona: ''
		},
		loginUser: {
			email: ''
		},
		persona: sessionStorage.getItem('persona') || '',
		activeTab: 'login',
		appNotice: false,
		serviceUrl: 'https://healthcraft.team.sh/'
	},
	methods: {
		personaChange(val) {
			this.persona = val;
			this.newUser.persona = val;
		},
		signUp: function () {
			console.log('POST: ', this.serviceUrl + 'signup', this.newUser);
			this.appNotice = true;
			axios.post(this.serviceUrl + 'signup', this.newUser).then(() => {
				alert('Posted the data, should we do a location.replace or will the server return a URL?');
			})
		},
		logIn: function () {
			console.log('POST: ', this.serviceUrl + 'login', this.newUser);
			axios.post(this.serviceUrl + 'login', this.newUser).then(() => {
				alert('Posted the data, should we do a location.replace or will the server return a URL?');
			})
		},
		confirmedAppDownload() {
			console.log('User has confirmed they have the CryptoPhoto app');
		}
	}
})
