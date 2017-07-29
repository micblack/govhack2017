<template>
	<el-select v-model="persona" placeholder="Choose a persona experience">
		<el-option
			v-for="personaOption in personas"
			:key="personaOption.value"
			:label="personaOption.label"
			:value="personaOption.value">
		</el-option>
	</el-select>
</template>

<script>
module.exports = {
	name: 'personas',
	props: [],
	watch: {
		persona: function (val) { 
			sessionStorage.setItem('persona', val);
			this.$emit('change', val);
		}
	},
	data() {
		return {
			personas: [{
				value: 'subscriber',
				label: 'Subscriber / Patient'
			}, {
				value: 'doctor',
				label: 'Doctor / Medical Professional'
			}, {
				value: 'warehouse',
				label: 'Warehouse / Pharmacy'
			}],
			persona: sessionStorage.getItem('persona') || ''
		}
	}
}
</script>

