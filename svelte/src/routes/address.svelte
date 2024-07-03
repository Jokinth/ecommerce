<script>
    import { replace } from "svelte-spa-router";import Nav from './navigate.svelte';
    const token = localStorage.getItem('token');
   let currentUserID = localStorage.getItem('userID') ;
   let  address = {
    street : "",
    city : "",
    state : "",
    country : ""
  };
   async function submit(event){
        event.preventDefault();
        let formData = {
        street: address.street,
        city: address.city,
        state: address.state,
        country: address.country
    };
        try {
      const response = await fetch(`http://127.0.0.1:8000/add_address`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      replace('/profile');

    } catch (error) {
      console.error('Error signing up:', error);
    }
    } 
</script>
<Nav/>
<form on:submit={submit}>
    <table border="1" style="margin-left: auto; margin-right : auto;">
        <tr><th colspan="2" align="left"><u><b>ADDRESS </b></u> </th></tr>
        <tr> <th> STREET :</th> <th> <input type = "text" bind:value={address.street} required> </th> </tr>
        <tr> <th> CITY :</th> <th> <input type = "text" bind:value={address.city} required> </th> </tr>
        <tr> <th> STATE :</th> <th> <input type = "text" bind:value={address.state} required> </th> </tr>
        <tr> <th> COUNTRY :</th> <th> <input type = "text" bind:value={address.country} required> </th> </tr>
        <tr> <th colspan="2" align="right">
            <input type="submit" value="add address">
        </th> </tr>
    </table>
</form>