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
				value: 'Subscriber / Patient',
				label: 'Subscriber / Patient'
			}, {
				value: 'Doctor / Medical Professional',
				label: 'Doctor / Medical Professional'
			}, {
				value: 'Warehouse / Pharmacy',
				label: 'Warehouse / Pharmacy'
			}],
			persona: sessionStorage.getItem('persona') || ''
		}
	}
}
</script>

