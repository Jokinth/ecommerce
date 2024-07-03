<script>
    import {replace} from 'svelte-spa-router'
   // import { writable } from 'svelte/store';
     let msg = 0
    let User={
        email : '',
        password : ''
    };
    function redirect_signin(){
      replace("/signup")
    }

    function redirect_pass(){
      replace("/forget_pass");
    }

    async function login_fun(event){
       event.preventDefault();
        let formData = {
        email: User.email,
        password: User.password,
      };
      try{
    let response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      if(data.msg == 'user not exist'){
        msg = "user not exist"
      }
      else{
        if(data.msg === "pass_worng"){
            msg = "give correct password"
        }
        else{
      localStorage.setItem('userID', data.user_id);
      localStorage.setItem('token', data.access_token); 
      localStorage.setItem('role', data.role);

      replace('/home');
    }}

    } catch (error) {
      console.error('Error signing up:', error);
    }}
</script>
<h1 style="text-align: center;">Log In </h1>
<form on:submit={login_fun}>
  <table style="margin-left: auto; margin-right : auto;">
    <tr><th>EMAIL :</th><th><input type="email" bind:value={User.email}></th></tr>
    <tr><th>PASSWORD :</th><th><input type="password" bind:value={User.password}></th></tr>
    <tr> <th colspan="2" align="right">
        <input type="submit" value="log in">
    </th> </tr>
    <tr> <th colspan="2" align="right">
      <button on:click={redirect_signin}>create account!</button>
  </th> </tr>
  <tr> <th colspan="2" align="right">
    <button on:click={redirect_pass}>forget password?</button>
</th> </tr>
  </table>  
</form>
{#if msg}
<p style="text-align: center;"><b>{msg}</b></p>
{/if}