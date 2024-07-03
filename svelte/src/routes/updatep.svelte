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

   async function remove(event , id){
    event.preventDefault();
    try{
    let response = await fetch(`http://127.0.0.1:8000/delete_product`, {
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
    </table></form>
