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
<div id='total'><Nav/>
<form on:submit={submit}>
    <table style="margin-left: auto; margin-right : auto;">
        <tr><th colspan="2"  align="left"><u><b>ADDRESS </b></u> </th></tr>
        <tr> <th> STREET :</th> <th> <input type = "text" bind:value={address.street} required> </th> </tr>
        <tr> <th> CITY :</th> <th> <input type = "text" bind:value={address.city} required> </th> </tr>
        <tr> <th> STATE :</th> <th> <input type = "text" bind:value={address.state} required> </th> </tr>
        <tr> <th> COUNTRY :</th> <th> <input type = "text" bind:value={address.country} required> </th> </tr>
        <tr> <th colspan="2" align="right">
            <input type="submit" value="add address">
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
        color: #010f01; /* Text color for the entire page */
    }
  form {
    width: 80%;
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }

  th {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }

  th {
    background-color: #f2f2f2;
    font-weight: bold;
  }

  input[type="text"] {
    width: calc(100% - 20px); /* Adjusted to account for padding */
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 14px;
  }

  input[type="submit"] {
    padding: 10px 20px;
    background-color: rgb(182, 37, 134); /* Green color similar to the edit form */
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
    float: right;
  }

  input[type="submit"]:hover {
    background-color: #45a049;
  }
</style>
