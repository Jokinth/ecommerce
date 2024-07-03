<script>
  import { onMount } from 'svelte';
  import Nav from './navigate.svelte';
  import { replace } from 'svelte-spa-router';

  let storedProductList = [];
  let total = 0;

  // Fetch stored product list on component mount
  onMount(() => {
    let currentUserID = localStorage.getItem('userID');
    storedProductList = JSON.parse(localStorage.getItem(`productList_${currentUserID}`)) || [];
    total = parseFloat(localStorage.getItem(`total_${currentUserID}`)) || 0;
    calculateTotal();
  });

  // Function to calculate total price
  function calculateTotal() {
    total = 0;
    storedProductList.forEach(item => {
      total += item.rate * item.quantity;
    });
    updateLocalStorage();
  }

  // Function to update local storage with product list and total
  function updateLocalStorage() {
    let currentUserID = localStorage.getItem('userID');
    localStorage.setItem(`productList_${currentUserID}`, JSON.stringify(storedProductList));
    localStorage.setItem(`total_${currentUserID}`, total.toFixed(2)); // Store total with two decimal places
  }

  // Function to remove a product from the list
  function remove(pid) {
    storedProductList = storedProductList.filter(item => item.id !== pid);
    calculateTotal(); // Update total after removal
  }
</script>

<Nav />
<br>
<h3>Items in your cart:</h3>

{#if storedProductList.length > 0}
  <div>
    <h2>Stored Product List:</h2>
    <ul>
      {#each storedProductList as { id, name, quantity, rate }}
        <li>Name: {name} Quantity: {quantity} Rate for one: {rate} <button on:click={() => remove(id)}>Remove</button></li>
      {/each}
    </ul>
    <button on:click={() => replace("/order")}>Order</button>
  </div>
  <h1>Total: {total}</h1>
{:else}
  <p>No products stored yet.</p>
{/if}
