<template>
  <w-progress v-show="show"></w-progress>
</template>

<script setup>
const { show } = defineProps(["show"]);
</script>

<style scoped></style>
