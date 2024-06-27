<script>
    import { replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';

    let currentUserID = localStorage.getItem('userID') ;
    
    let name;

    async function change(){
        let formData = {
        user_name: "",
        email: name,
        password: "",
        mobile_number: "",
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
        replace("/profile");
    }
    catch (error) {
      console.error( error);
    }}
</script>
<Nav/>
<form on:submit={change}>
    <table style="margin-left: auto;margin-right:auto">
        <tr><th>Enter email to be changed : </th><th> <input type = "text" bind:value={name}> </th></tr>
        <tr> <th colspan="2" align="right">
            <input type="submit" value="save">
        </th> </tr>
    </table>
</form>
