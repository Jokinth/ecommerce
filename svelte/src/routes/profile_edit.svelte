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
    let user_address = [];

    function add_address(){
      replace('/add_address');
    }

function edit(){
      replace('/edit');
    }

    async function always_run(){
    try{
    let response = await fetch(`http://127.0.0.1:8000/get_user/${currentUserID}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
       let data = await response.json();
       user = data;
    }
    catch (error) {
      console.error( error);
    }
    try{
    let response = await fetch(`http://127.0.0.1:8000/get_address/${currentUserID}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
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
<Nav />
<form on:submit={edit}>
  <table style="margin-left: auto; margin-right : auto;">
    <tr><th>NAME : </th><th>{user.name}</th></tr>
    <tr><th>E-MAIL : </th><th>{user.email}</th> </tr>
    <tr><th>MOBILE NUMBER : </th><th>{user.mobile_number}</th> </tr>
    <tr><th>change password : </th><th>******</th></tr>
    <tr> <th colspan="2" align="right">
      <input type="submit" value="edit"></th></tr>
    </table>
    </form>
    
<form>
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
</form>