<script>
    import { replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';
    function create(){
        replace('/createp');
    }
    function update(){
        replace('/updatep');
    }
</script>
<Nav /><br>

<div id='createUpdateComponent'>
    <h1>what do you want to do ?</h1><br>
<button on:click={create}>create product</button><br>
<button on:click={update}>update product</button><br>
</div>

<style>
  /* CSS for the Create/Update Component */
  #createUpdateComponent {
    color: rgb(116, 9, 9);
    padding: 20px;
    margin: 20px auto;
    width: 80%;
    max-width: 600px;
    text-align: center;
  }

  h1 {
    text-decoration: dashed;
  }

  button {
    padding: 8px 16px;
    background-color: rgb(182, 37, 134);
    color: wheat;
    border: none;
    border-radius: 100px;
    cursor: pointer;
    margin-bottom: 10px;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #45a049;
  }
</style>