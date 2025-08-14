<template>
  <div>
    <h1>ТЕСТ НАСТРОЕК</h1>
    <p>Компонент работает!</p>
  </div>
</template>

<script>
export default {
  name: 'TestSettings',
  render() {
    return h('div', [
      h('h1', 'ТЕСТ НАСТРОЕК'),
      h('p', 'Компонент работает!')
    ])
  }
}
</script>
