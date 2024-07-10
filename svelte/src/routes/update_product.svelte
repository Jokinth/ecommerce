<script>
    import {replace} from 'svelte-spa-router';
    import Nav from './navigate.svelte';

 let id = localStorage.getItem('pid') ;
    $: id = id;
    const token = localStorage.getItem('token');
   
    let p = {
        name : "" ,
        price : 0 ,
        availale: 0 ,
        category: "" ,
        brand: "" ,
        descrition: "" };
        
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
      const response = await fetch(`http://127.0.0.1:8000/update_product/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      replace('/updatep');
    } catch (error) {
      console.error('Error signing up:', error);
    }
    }
</script><body>
<Nav /><br>
<h1>edit product</h1>
<br><form on:submit={p_create}>
    <table>
        <tr><th>name:</th><th><input type="text" bind:value={p.name}></th></tr>
        <tr><th>price:</th><th><input type="number" bind:value={p.price}></th></tr>
        <tr><th>quantity availale:</th><th><input type="number" bind:value={p.availale}></th></tr>
        <tr><th>catogery:</th><th><input type="text" bind:value={p.category}></th></tr>
        <tr><th>brand:</th><th><input type="text" bind:value={p.brand}></th></tr>
        <tr><th>descrition:</th><th><input type="text" bind:value={p.descrition}></th></tr>
        <tr> <th colspan="2" align="right">
            <input type="submit" value="update product">
        </th> </tr>
    </table>
</form></body>
<style>
  body {
    overflow: auto;
    background: linear-gradient(to bottom, #d47d19, #a50b58);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}


h1 {
    text-align: center;
    color: #fff;
    text-decoration: underline;
    margin-bottom: 20px;
  }

  form {
    width: 80%;
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }

  th {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }

  th {
    background-color: #f2f2f2;
    font-weight: bold;
  }

  input[type="text"],input[type="number"] {
    width: calc(100% - 20px); 
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
  }

  input[type="submit"] {
    padding: 10px 20px;
    background-color: rgb(182, 37, 134);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }

  input[type="submit"]:hover {
    background-color: #45a049;
  }
</style>