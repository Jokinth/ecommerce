<script>
  import { onMount } from 'svelte';
  import { replace } from 'svelte-spa-router';
  import Nav from './navigate.svelte';

const token = localStorage.getItem('token');
  let currentUserID = localStorage.getItem('userID');
  let user_address = [];
  let total = localStorage.getItem(`total_${currentUserID}`) || 0;
  let storedProductList = JSON.parse(localStorage.getItem(`productList_${currentUserID}`)) || [];

  let selectedAddress = null;

  async function fetchAddresses() {
    try {
      const response = await fetch(`http://127.0.0.1:8000/get_address`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      user_address = data.addresses;
    } catch (error) {
      console.error('Error fetching addresses:', error);
    }
  }

  async function updateProducts() {
    try {
      for (let i = 0; i < storedProductList.length; i++) {
        let ava = parseInt(storedProductList[i].available) - parseInt(storedProductList[i].quantity);
         
        if(ava == 0){
          ava = -1;
        }
        const formData1 = {
          pname: "",
          price: 0,
          quantity_available: ava,
          category: "",
          brand: "",
          description: ""
        };

        const response = await fetch(`http://127.0.0.1:8000/update_product/${storedProductList[i].id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(formData1)
        });

        if (!response.ok) {
          throw new Error(`Failed to update product ${id}`);
        }

        const updatedProduct = await response.json();
      }
    } catch (error) {
      console.error('Error updating products:', error);
      throw error; // Rethrow the error to handle it in the order function
    }}
  

  async function placeOrder() {
    let formData = {
          uid : currentUserID,
          total_rate : total,
          address : selectedAddress
        };
    try {
      const response = await fetch('http://127.0.0.1:8000/pot_order', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Failed to place order');
      }

      const orderResponse = await response.json();
      replace('/sucess'); // Redirect to success page after successful order
    } catch (error) {
      console.error('Error placing order:', error);
      // Handle error or provide user feedback
    }
  }
let products = [];
let product_id=[]
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
      product_id = data.map(product => product.pid);
    } catch (error) {
      console.error(error);
    }
  }
  
  let c=0;
  function checkQuantity() {
    
    for (let i = 0; i < storedProductList.length; i++) {
        if ( !product_id.includes(storedProductList[i].id) ) {
          alert('no');  
          return false; 
        }
        if (storedProductList[i].available < storedProductList[i].quantity) {
            return false;
        }
    }
    return true;
}

  async function order(event) {
    event.preventDefault();

    if (checkQuantity()) {
      try {
        // First, update products
        await updateProducts();

        await placeOrder();
      } catch (error) {
        console.error('Error ordering:', error);
        // Handle error or provide user feedback
      }
    } else {
      alert("Check the quantity! Some products are out of stock.");
    }
  }

  // Fetch addresses on component mount
  onMount(fetchAddresses);
  onMount(fetchProducts);
  function selectedAddress_(event){
    selectedAddress = event.target.value;
  }
</script>
<div id='total'>
<Nav /><br><br>

<h1><b>Order details:</b></h1>

<form on:submit={order}>
  <table >
    <tr>
      <th>Details of the products</th>
      <th>
        <ol>
          {#each storedProductList as { id, name, quantity, available,rate }}
            <li>Name: {name} Quantity: {quantity} Rate for one: {rate} available:{available}</li>
          {/each}
        </ol>
      </th>
    </tr>
    <tr>
      <th>Choose your address:</th>
      <th>
        {#each user_address as address }
          <div>
            <input type="radio" name="address" value="{address.city}, {address.state}, {address.country}, {address.street}" on:change={selectedAddress_} required>
            {address.city}, {address.state}, {address.country}, {address.street}
          </div>
        {/each}
      </th>
    </tr>
    <tr>
      <th>Total amount :</th>
      <th>{total}</th>
    </tr>
    <tr>
      <th colspan="2" align="right">
        <input type="submit" value="Buy now">
      </th>
    </tr>
  </table>
</form></div>
<style>
  /* General styles */
  th {
    text-align: center;
    padding: 10px;
  }

  /* Form and table styles */
  form {
    color: #010f01;
    margin: 20px auto;
    width: 80%; /* Adjust width as needed */
    padding: 20px;
    border: 1px solid #031103;
    border-radius: 5px;
    background-color: wheat;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  table {
    width: 100%;
    margin-top: 10px;
    border-collapse: collapse;
  }

  table th {
    padding: 10px;
    border: 1px solid #ccc;
  }

  table th {
    text-align: center;
    background-color: #f2f2f2; /* Light gray background for headers */
  }

 
  table input[type="radio"] {
    margin-right: 10px;
    vertical-align: middle;
  }

  table input[type="submit"] {
    padding: 10px 16px;
    background-color: rgb(182, 37, 134);
    color: wheat;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  table input[type="submit"]:hover {
    background-color: #45a049;
  }

  /* Additional styles */
  

  #total {overflow: auto;
    background: linear-gradient(to bottom, #d47d19, #a50b58);
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
