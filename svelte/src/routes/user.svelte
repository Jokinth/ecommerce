<script>
  import { replace } from 'svelte-spa-router';
  import Nav from './navigate.svelte';

  let products = [];
  let quantity_required = [];

  let currentUserID = localStorage.getItem('userID');
  let productList = JSON.parse(localStorage.getItem(`productList_${currentUserID}`)) || [];

  async function fetchProducts() {
    try {
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
    } catch (error) {
      console.error(error);
    }
  }

  async function add_to_cart(event, name, id , rate , available ,quantity) {
    event.preventDefault();
    if(available >= quantity){
      if (!productList.some(item => item.id === id)) {
        productList.push({ id , name , rate , available , quantity });
        localStorage.setItem(`productList_${currentUserID}`, JSON.stringify(productList));
      } else {
        alert("already in cart");
      }
      replace('/cart');
    } else {
      alert("no stock");
    }
  }

  fetchProducts();

function  view_product(pid){
  
  localStorage.setItem('current_product', pid);
  replace('/view');
}

</script>

<Nav />
<br>
<button on:click={() => replace('/cart')} style="position: fixed; top: 30px; right: 190px; padding: 10px 20px">Cart</button>
<button on:click={() => replace('/history')} style="position: fixed; top: 30px; right: 270px; padding: 10px 20px">Order History</button>
<h1>Products:</h1>
<form>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Price</th>
        <th>Quantity Available</th>
        <th>Category</th>
        <th>Brand</th>
        <th>Description</th>
        <th>Add to Cart</th>
      </tr>
    </thead>
    <tbody>
      {#each products as product, i}
        <tr>
          <td>{product.pname}</td>
          <td>{product.price}</td>
          <td>{product.quantity_available}</td>
          <td>{product.category}</td>
          <td>{product.brand}</td>
          <td>{product.description}</td>
          <td>
            <input type="number" bind:value={quantity_required[i]} >
            <button on:click={(event) => add_to_cart(event, product.pname , product.pid , product.price , product.quantity_available , quantity_required[i])} >Add to Cart</button>
          </td>
        <td> <button on:click={() => view_product(product.pid)}>view</button>
        </td>
      </tr>
      {/each}
    </tbody>
  </table>
</form>
