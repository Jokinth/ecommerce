<script>
    import {replace} from 'svelte-spa-router';
    import Nav from './navigate.svelte';
    let products = [];
    const token = localStorage.getItem('token');
async function always_run(){
    try{
    let response = await fetch(`http://127.0.0.1:8000/read_product`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
       let data = await response.json();
       products = data;
    }
    catch (error) {
      console.error( error);
    }
    }always_run();

   async function remove(event,pid){
    event.preventDefault();
    try{
    let response = await fetch(`http://127.0.0.1:8000/delete_product/${pid}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
       let data = await response.json();
       alert(data.msg);
       always_run();
    }
    catch (error) {
      console.error( error);
    }
   }
   function edit(event , id){
    //event.preventDefault();
    localStorage.setItem('pid', id);
    replace("/update_product");
   }

</script>
<body>
<Nav /><br>
<h1>products:</h1>
<form><table>
    <tr><th> name </th><th> price </th><th> quantity_available </th><th> category </th><th> brand </th><th> description </th><th> edit </th><th> remove </th></tr>
     <br> {#each products as product }
      <tr><th>{product.pname}</th><th> {product.price}</th><th>{product.quantity_available}</th><th> {product.category}</th><th> {product.brand}</th><th> {product.description}</th>
        <th><button on:click={(event) => edit(event,product.pid)}>edit</button>
        </th> <th><button on:click={(event) => remove(event,product.pid)}>remove</button></th>
    </tr>
      {/each}
    </table>
  </form>
  </body>
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
      width: 100%;
      max-width: 800px;
      margin: 20px auto;
      padding: 20px;
      border-radius: 8px;
      background-color: wheat;
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
  
  
button {
      padding: 10px 20px;
      background-color: rgb(182, 37, 134);
      color: #fff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 16px;
      transition: background-color 0.3s ease;
    }
  
    button:hover {
      background-color: #45a049;
    }
  </style>