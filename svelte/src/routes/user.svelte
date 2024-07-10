<script>
  import { replace } from 'svelte-spa-router';
  

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
<body>

<button id='cart' on:click={() => replace('/cart')}>Cart</button>
<button id='order' on:click={() => replace('/history')}>Order History</button>
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
        <th>view product</th>
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
</body><style>
  h1 {
    color: rgb(116, 9, 9);
    text-decoration: underline;
  }

  #cart,
  #order {
    padding: 8px 16px;
    background-color: rgb(182, 37, 134);
    color: wheat;
    border: none;
    border-radius: 100px;
    cursor: pointer;
    position: fixed;
    top: 30px;
  }

  #cart {
    right: 220px;
  }

  #order {
    right: 290px;
  }

  #cart:hover,
  #order:hover {
    background-color: #45a049; 
  }

  table {
    width: 100%;
    margin: 20px auto; 
    padding: 20px;
    border: 1px solid #48d348;
    border-radius: 5px;
    background-color: wheat;
  }

  table th,
  table td {
    text-align: center;
    padding: 8px;
  }

  table button {
    padding: 8px 16px;
    background-color: rgb(182, 37, 134);
    color: wheat;
    border: none;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  table button:hover {
    background-color: #45a049; 
  }

  table input[type="number"] {
    width: 100px; 
    padding: 6px;
    border: 1px solid #ccc;
    border-radius: 3px;
  }
</style>
