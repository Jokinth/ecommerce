<script>
    import { replace } from "svelte-spa-router";
    import Nav from './navigate.svelte';
    import Product from './product.svelte';
    import User from './user.svelte';
    let user = localStorage.getItem('role') ;
    $: user = user;

    function log_out(){
     replace('/logout');  
    }
    function profile(){
     replace('/profile');  
    }
    
</script>
<Nav /><br>
<h1>HOME PAGE</h1>
<div id = "log"><button on:click={log_out}>LOGOUT</button>  <button on:click={profile}>Profile</button></div>
{#if user == "user"}
<User />
{:else}
<Product />
{/if}
<style>
    h1{
        text-align: center;
    }
    #log{
        position: fixed; 
        top: 20px; 
        right: 20px; 
        padding: 10px 20px
    }
    </style>