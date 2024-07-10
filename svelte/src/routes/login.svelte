<script>
  import { replace } from 'svelte-spa-router';

  let msg = '';
  let User = {
    email: '',
    password: ''
  };

  function redirect_signin() {
    replace('/signup');
  }

  function redirect_pass() {
    replace('/forget_pass');
  }

  async function login_fun(event) {
    event.preventDefault();
    let formData = {
      email: User.email,
      password: User.password
    };

    try {
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

      if (data.msg === 'user not exist') {
        msg = 'User does not exist';
      } else if (data.msg === 'pass_worng') {
        msg = 'Incorrect password';
      } else {
        localStorage.setItem('userID', data.user_id);
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('role', data.role);
        localStorage.setItem('exp', data.exp);

        replace('/home');
      }
    } catch (error) {
      console.error('Error signing in:', error);
    }
  }
</script>
<style>
  h1 {
    color: rgb(14, 11, 5);
    text-align: center;
    margin-top: 20px;
    text-decoration: underline;
  }

  form {
    color: #010f01;
    margin: 20px auto;
    width: 300px;
    padding: 20px;
    border: 1px solid #031103;
    border-radius: 5px;
    background-color: wheat;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  table {
    width: 100%;
    margin-top: 10px; 
  }

  table th {
    text-align: right;
    padding: 8px;
  }

  table input[type="email"],
  table input[type="password"] {
    width: calc(100% - 16px); 
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;     transition: border-color 0.3s ease; 
  }

  table input[type="email"]:focus,
  table input[type="password"]:focus {
    border-color: rgb(182, 37, 134); 
    outline: none; 
  }

  table input[type="submit"] {
    padding: 10px 16px;
    background-color: rgb(182, 37, 134);
    color: wheat;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease; 
  }

  table input[type="submit"]:hover {
    background-color: #45a049;
  }

  table button {
    background: none;
    border: none;
    cursor: pointer;
    color: #063a6e;
    text-decoration: underline;
    transition: color 0.3s ease; 
  }

  table button:hover {
    color: rgb(182, 37, 134); 
    text-decoration: none;
  }

  .message {
    text-align: center;
    margin-top: 10px;
    color: rgb(248, 42, 6);
    font-weight: bold;
  }

  #total {
    background: linear-gradient(to bottom, #d47d19, #a50b58);
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center; 
    align-items: center; 
  }
</style>

<div id ="total">
<h1>Log In</h1>
<form on:submit={login_fun}>
  <table>
    <tr><th>EMAIL ID:</th><th><input type="email" bind:value={User.email}></th></tr>
    <tr><th>PASSWORD: </th><th><input type="password" bind:value={User.password}></th></tr>
    <tr><th colspan="2" align="right"><input type="submit" value="Log In"></th></tr>
    <tr><th colspan="2" align="right"><button on:click={redirect_signin}>Create Account!</button></th></tr>
    <tr><th colspan="2" align="right"><button on:click={redirect_pass}>Forget Password?</button></th></tr>
  </table>
</form>

{#if msg}
<p class="message">{msg}</p>
{/if}
</div>