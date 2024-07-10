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
<div id='total'>
<Nav />
<br>
<b>
<h2><u>Items in your cart:</u></h2>
</b>
{#if storedProductList.length > 0}
  <div id='list'>
    <form><table>
       <thead> <tr><th><b><u>Name</u></b></th><th><b><u>Quantity</u></b></th><th><b><u>Rate for one</u></b></th><th><b><u>Remove</u></b></th></tr></thead><tbody>
      {#each storedProductList as { id, name, quantity, rate }}
        <tr><td>{name} </td><td>{quantity} </td><td>{rate} </td><td><button on:click={() => remove(id)}>Remove</button></td></tr>
      {/each}</tbody>
    </table></form>
    <button id='order' on:click={() => replace("/order")}>Order</button>
  </div>
  <h1><b>Total: {total}</b></h1>
{:else}
  <p><b>No products stored yet.</b></p>
{/if}
</div>
<style>
  #total {
    overflow: auto;
    background: linear-gradient(to bottom, #d47d19, #a50b58);
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #010f01; /* Text color for the entire page */
  }
  table th {
    padding: 8px;
    font-weight: bold; /* Font weight for table headings */
  }

  table td {
    padding: 8px;
    font-size: medium; /* Font weight for table data */
  }
  #list {
    margin: 20px auto;
    width: 1000px;
    padding: 20px;
    border: 1px solid #031103;
    border-radius: 5px;
    background-color: wheat;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    position: relative; /* Position relative to contain absolutely positioned elements */
  }

  table {
    width: 100%;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 20px;
  }

  table th{
    padding: 8px;
  }

  h1 {
    position: fixed;
    top: 20px;
    right: 100px;
    color: #010f01; /* Text color for the total */
  }

  button {
    padding: 8px 16px;
    background-color: rgb(211, 15, 152);
    color: wheat;
    border: none;
    border-radius: 3px;
    cursor: pointer;
  }
  button:hover{
    background-color: green;
  }

  #order {
    position: absolute;
    bottom: -60px; /* Adjusted to position just below the table */
    right: 20px; /* Aligned to the right of the table container */
  }
</style>
