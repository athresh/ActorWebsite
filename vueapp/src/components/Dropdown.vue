<template>
  <div class="dropdown">
    <select
      @input="event => { $emit('input', event.target.value) }"
      >
      <option v-for="(option, name) in options" :value="option">{{ name }}</option>
    </select>
  </div>
</template>

<script>
export default {
  props: {
    value: null,
    options: {
      type: Object,
      required: true
    }
  },
}

</script>