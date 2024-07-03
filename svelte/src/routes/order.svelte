<script>
  import { onMount } from 'svelte';
  import { replace } from 'svelte-spa-router';
  import Nav from './navigate.svelte';
let a=0;
  let currentUserID = localStorage.getItem('userID');
  let user_address = [];
  let total = localStorage.getItem(`total_${currentUserID}`) || 0;
  let storedProductList = JSON.parse(localStorage.getItem(`productList_${currentUserID}`)) || [];

  let selectedAddress = null;

  async function fetchAddresses() {
    try {
      const response = await fetch(`http://127.0.0.1:8000/get_address/${currentUserID}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
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
        if(ava == 0){ava = -1;}
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
            'Content-Type': 'application/json'
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
</form>
<style>
  th{
    text-align: center;
    padding: 10px;
  }
</style>
<!--{#each product_id as id , i}
          <div>
          <h1>{id}</h1>
          <h1>{storedProductList[i].id}</h1></div>
        {/each}-->
        