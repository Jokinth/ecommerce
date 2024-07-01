<script>
  import Nav from './navigate.svelte';
    let a=0;
    let p = {
        name : " " ,
        price : " " ,
        availale: " " ,
        category: " " ,
        brand: " " ,
        descrition: " " };
        
async function p_create(event){
        
    event.preventDefault();
        
        let formData = {
        pname : p.name ,
        price : parseInt(p.price) ,
        quantity_available: parseInt(p.availale) ,
        category: p.category ,
        brand: p.brand ,
        description: p.descrition
    };
        try {
      const response = await fetch('http://127.0.0.1:8000/create_product', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      if(data.msg == "created"){
        a = 1;
      }
    } catch (error) {
      console.error('Error signing up:', error);
    }
    }
</script>
<Nav /><br>
<h1>create product</h1>
<br><form on:submit={p_create}>
    <table>
        <tr><th>name:</th><th><input type="text" bind:value={p.name}></th></tr>
        <tr><th>price:</th><th><input type="number" bind:value={p.price}></th></tr>
        <tr><th>quantity availale:</th><th><input type="number" bind:value={p.availale}></th></tr>
        <tr><th>catogery:</th><th><input type="text" bind:value={p.category}></th></tr>
        <tr><th>brand:</th><th><input type="text" bind:value={p.brand}></th></tr>
        <tr><th>descrition:</th><th><input type="text" bind:value={p.descrition}></th></tr>
        <tr> <th colspan="2" align="right">
            <input type="submit" value="create product">
        </th> </tr>
    </table>
</form>
{#if a== 1}
<h1>created</h1>
{/if}