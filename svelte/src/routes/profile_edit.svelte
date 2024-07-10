<script>
    import { replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';

    let user ={
        name : "",
        email : "",
        mobile_number : ""
    }
    let currentUserID = localStorage.getItem('userID') ;
    $: currentUserID = currentUserID;
    const token = localStorage.getItem('token');
    let user_address = [];

    function add_address(){
      replace('/add_address');
    }

function edit(){
      replace('/edit');
    }

    async function always_run(){
      try {
  const response = await fetch('http://127.0.0.1:8000/get_user', {
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
  user = data;
} catch (error) {
  console.error('Error fetching user data:', error);
}

    
    try{
    let response = await fetch(`http://127.0.0.1:8000/get_address`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
       let data = await response.json();
       user_address = data.addresses;
    }
    catch (error) {
      console.error( error);
    }
  }
    always_run();
</script>
<div id='total'><Nav />
<form on:submit={edit} id="userInfoForm">
  <table style="margin-left: auto; margin-right : auto;">
    <tr><th>NAME : </th><th>{user.name}</th></tr>
    <tr><th>E-MAIL : </th><th>{user.email}</th> </tr>
    <tr><th>MOBILE NUMBER : </th><th>{user.mobile_number}</th> </tr>
    <tr><th>change password : </th><th>******</th></tr>
    <tr> <th colspan="2" align="right">
      <input type="submit" value="edit"></th></tr>
    </table>
    </form>
    
<form id="userAddressForm">
  <table style="margin-left: auto; margin-right : auto;">
    <tr><th>adresses:</th>
      <th>
        <ol>
        {#each user_address as address }
          <li><div>{address.city}, {address.state}, {address.country}, {address.street}</div></li>
        {/each}
      </ol></th></tr>
      <tr> <th colspan="2" align="right">
        <button on:click={add_address}>add address</button>
    </th> </tr>
  </table>
</form></div>
<style>
  
  #total {
    overflow: auto;
    background: linear-gradient(to bottom, #d47d19, #a50b58);
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: rgb(116, 9, 9);
    padding: 20px;
  }

  
  #userInfoForm, #userAddressForm {
    width: 80%;
    max-width: 600px;
    background-color: wheat;
    border: 1px solid #48d348;
    border-radius: 5px;
    padding: 20px;
    margin-bottom: 20px;
  }

  table {
    width: 100%;
    text-align: left;
    border-collapse: collapse;
    margin-bottom: 20px;
  }

  th {
    padding: 8px;
    border-bottom: 1px solid #ddd;
    background-color: #f2f2f2;
    text-align: left;
  }

  input[type="submit"], button {
    padding: 8px 16px;
    background-color: rgb(182, 37, 134);
    color: wheat;
    border: none;
    border-radius: 100px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  input[type="submit"]:hover, button:hover {
    background-color: #45a049;
  }

  ol {
    padding-left: 20px;
  }

  li {
    margin-bottom: 8px;
  }
</style>