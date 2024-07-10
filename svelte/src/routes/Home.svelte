<script>
    import { replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';
    import Product from './product.svelte';
    import User from './user.svelte';
    let user = localStorage.getItem('role');
    $: user = user;

    function log_out(){
        replace('/logout');  
    }
    function profile(){
        replace('/profile');  
    }
</script>

<body>
  
    <Nav /><br><br><br>
    <h1>HOME PAGE</h1>
    <div id="log">
        <button on:click={log_out} id="logout">LOGOUT</button>
        <button on:click={profile} id="profile">Profile</button>
    </div>


{#if user == "user"}
    <User />
{:else}
    <Product />
{/if}
<br><br><br><br><br><br><br><br><br><br><br><br>
</body>
<style>
    h1 {
      text-align: center;
      color: rgb(116, 9, 9);
      text-decoration: underline;
    }
  
    #log {
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 10px 20px;
    }
  
    #logout,
    #profile {
      position:sticky;
      top:0;
      padding: 8px 16px;
      background-color: rgb(182, 37, 134);
      color: wheat;
      border: none;
      border-radius: 100px;
      cursor: pointer;
    }
  
    body {
      overflow: auto;
      background: linear-gradient(to bottom, #d47d19, #a50b58);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  </style>
  
