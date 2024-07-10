<script>
    import { push, replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';
    let currentUserID = localStorage.getItem('userID') ;
    const token = localStorage.getItem('token');
    
    let profile = {
        user_name: "",
        email: "",
        password: "",
        mobile_number: ""
    };

    async function change(event){
      event.preventDefault();
        let formData = {
        user_name: profile.user_name,
        email: profile.email,
        password: profile.password,
        mobile_number: profile.mobile_number
      };
        try{
    let response = await fetch(`http://127.0.0.1:8000/edit`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
        push("/profile");
    }
    catch (error) {
      console.error( error);
    }}
</script>
<div id='total'><Nav/><br>
<h1>only give the field which is to be changed!!</h1>
<form on:submit={change}>
    <table style="margin-left: auto;margin-right:auto">
        <tr><th>Enter  name to be changed : </th><th> <input type = "text" bind:value={profile.user_name}> </th></tr>
        <tr><th>Enter  password to be changed : </th><th> <input type = "text" bind:value={profile.password} ></th></tr>
        <tr><th>Enter email to be changed : </th><th> <input type = "text" bind:value={profile.email}> </th></tr>
        <tr><th>Enter  mobile number to be changed : </th><th> <input type = "text" bind:value={profile.mobile_number}> </th></tr>
        <tr> <th colspan="2" align="right" id='save'>
            <input type="submit" value="save">
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

  h1 {
    text-align: center;
    color: #fff;
    text-decoration: underline;
    margin-bottom: 20px;
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
#save{
  text-align: right;
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
    background-color: rgb(182, 37, 134);
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }

  input[type="submit"]:hover {
    background-color: #45a049;
  }
</style>
