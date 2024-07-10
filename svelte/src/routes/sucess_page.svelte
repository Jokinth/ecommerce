<script>
    import Nav from './navigate.svelte';
</script>

<style>
  
  #container {
    background: linear-gradient(to bottom, #d47d19, #a50b58);
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: white;
    text-align: center;
  }

  h1 {
    font-size: 40px;
    margin-top: 20px;
    color :  #0d1106;
    font-family: fantasy;
  }

  
</style>

<div id="container">
    <Nav />
    <br /><br />
    <h1>Order placed successfully!!!</h1>
</div>
