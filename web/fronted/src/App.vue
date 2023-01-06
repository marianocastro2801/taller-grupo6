<template>
  <div>
      <table>

        <body>
          <tr>
              <td>   celda </td>
              <td>   celda </td>
              <td>   celda </td>
          </tr>
         
        </body>

      </table>

  </div>

</template>

<script>
import axios from "axios";
export default {
  /* name: 'App'  */ 
  data(){
    return {todos: null }
  },

  mounted(){
    console.log('hola mundo')
    this.getTodos()

  },

  methods(){
      getTodos()
          console.log('aqui va el codigo')
      

  }

}
</script>

<style>

</style>
