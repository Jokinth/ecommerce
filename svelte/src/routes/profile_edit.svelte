<script>
    import { replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';

    let user ={
        name : "",
        email : "",
        mobile_number : ""
    }
    let currentUserID = localStorage.getItem('userID') ;
   // let currentUserID = parseInt(currentUserID1, 10);
    $: currentUserID = currentUserID;
    let user_address = [];

    function name_edit(){
      replace('/profile/edit_name');
    }

    function email_edit(){
      replace('/profile/edit_email');
    }

    function mobile_edit(){
      replace('/profile/edit_mobile');
    }

    function pass_edit(){
      replace('/profile/edit_pass');
    }

    function add_address(){
      replace('/profile/add_address');
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
<form>
  <table style="margin-left: auto; margin-right : auto;">
    <tr><th>NAME : </th><th>{user.name}</th> <th><button on:click={name_edit}>edit</button></th></tr>
    <tr><th>E-MAIL : </th><th>{user.email}</th> <th><button on:click={email_edit}>edit</button></th> </tr>
    <tr><th>MOBILE NUMBER : </th><th>{user.mobile_number}</th> <th><button on:click={mobile_edit} >edit</button></th> </tr>
    <tr><th>change password : </th><th><button on:click={pass_edit}>change password</button></th></tr>
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