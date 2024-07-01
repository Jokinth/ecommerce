<script>
    import { push, replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';
    let currentUserID = localStorage.getItem('userID') ;
    
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
    let response = await fetch(`http://127.0.0.1:8000/edit/${currentUserID}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
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
<Nav/><br>
<h1>only give the field which is to e changed!!</h1>
<form on:submit={change}>
    <table style="margin-left: auto;margin-right:auto">
        <tr><th>Enter  name to be changed : </th><th> <input type = "text" bind:value={profile.user_name}> </th></tr>
        <tr><th>Enter  password to be changed : </th><th> <input type = "text" bind:value={profile.password} ></th></tr>
        <tr><th>Enter email to be changed : </th><th> <input type = "text" bind:value={profile.email}> </th></tr>
        <tr><th>Enter  mobile number to be changed : </th><th> <input type = "text" bind:value={profile.mobile_number}> </th></tr>
        <tr> <th colspan="2" align="right">
            <input type="submit" value="save">
        </th> </tr>
    </table>
</form>
